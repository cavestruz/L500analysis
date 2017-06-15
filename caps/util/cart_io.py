#!/usr/bin/python

import sys
import logging
from re import search
from glob import glob

import numpy as np
import pandas as pd

from numpy import fromfile

def read_aexp_list_from_files(directory, filename_prefix="halo_catalog_a", filename_suffix=".dat") :

    epochs = []
    for output in glob("%s/%s*%s" % (directory, filename_prefix, filename_suffix)) :
        search_string = filename_prefix+"(\d\.\d\d\d\d)"+filename_suffix
        epochs.append( float(search(search_string, output).group(1)) )

    return sorted(epochs)[::-1]

def read_halo_ids_from_file(filename) :

    h_ids = []

    with open(filename,"r") as f_input :

        for line in f_input.readlines() :
            cols = line.split()
            h_ids.append(int(cols[0]))

    return h_ids


def read_halo_catalog(directory, aexp, filename_prefix = "halo_catalog_a") :
    """
    loads halos from halo_catalog_a*.dat files
    """

    filename = "%s/%s%0.4f.dat" % (directory, filename_prefix, aexp)

    columns = ["id", "x", "y", "z", "vx", "vy", "vz", "r_hc", 
               "M_hc", "num_particles", "vmax_hc", "rmax_hc"] 

    halo_catalog = pd.read_table(filename, sep=r"\s+", 
                                 skiprows=10, names=columns)

    halo_catalog["aexp"] = aexp

    return halo_catalog

def load_halo_catalog_data(sim, directory, aexp, h_inverse,  mass_cut = 0.0, halo_list = []) :

    halo_data = read_halo_catalog(directory, aexp)

    if mass_cut :
        halo_data = halo_data[halo_data["M_hc"] > mass_cut]

    if halo_list :
        halo_data = halo_data[halo_data["id"] in halo_list]

    add_remove_h_inverse(halo_data, h_inverse, "in_halo_catalog")
    comoving_physical_swap(halo_data, aexp, comoving_to_physical=True)

    return halo_data


def read_halo_list(directory, aexp, radii = ["vir", "200c", "200m"],
                   filename_prefix = "halo_list") :

    # id R_vir(Delta) [kpc/h physical] M_dark M_gas 
    # M_gas_cold M_star M_star_new M_baryon M_total (< R_vir(Delta))
    # M_total(catalog) [M_sun/h] V_circ_max [km/s physical] 
    # R(V_circ_max) [kpc/h physical] gas-Z_II_ave gas-Z_Ia_ave star-Z_II_ave 
    # star-Z_Ia_ave star_new-Z_II_ave star_new-Z_Ia_ave [wrt solar] star-age_ave [Gyr]

    halo_lists = None
    
    for radius in radii :
        columns = ["id", "r"+radius, "M_dark_"+radius, "M_gas_"+radius,
                   "M_gas_cold_"+radius, "M_star_"+radius, "M_star_new_"+radius,
                   "M_baryon_"+radius, "M_total_"+radius, "M_total_hc",
                   "vmax_"+radius, "rmax_"+radius, 
                   "gas-Z_II_avg_"+radius, "gas-Z_Ia_avg_"+radius, 
                   "star-Z_II_avg_"+radius, "star-Z_Ia_avg_"+radius,
                   "star_new-Z_II_avg_"+radius, "star_new-Z_Ia_avg_"+radius,
                   "star-age_avg_"+radius]

        filename = "%s/%s_%s_a%0.4f.dat" % (directory, filename_prefix,
                                            radius, aexp)

        halo_list = pd.read_table(filename, sep=r"\s+", 
                                  skiprows=6, names=columns)

        #remove extra hc mass column
        halo_list = halo_list.drop('M_total_hc',1)

        if halo_lists is None :
            halo_lists = halo_list
        else :
            halo_lists = pd.merge(halo_lists, halo_list)

    halo_lists["aexp"] = aexp
    return halo_lists


def load_halo_list_data(sim, directory, aexp, radii, h_inverse,
                        mass_cut = 0.0, halo_list = []) :

    halo_data = read_halo_list(directory, aexp, radii = radii)

    if mass_cut :
        halo_data = halo_data[halo_data["M_hc"] > mass_cut]

    if halo_list :
        halo_data = halo_data[halo_data["id"] in halo_list]

    add_remove_h_inverse(halo_data, h_inverse, "in_profiles")

    return halo_data

def load_profiles_data(sim, directory, aexp, h_inverse,
                      mass_cut = 0.0, halo_list = [],
                      profile_types = ["gas", "mass", "velocity"]) :

    if mass_cut :
        halo_list = sim.get_halo_ids(aexp=aexp, mass_cut=mass_cut,
                                    halo_catalog = True)
        if len(halo_list):
            print "loading profiles for %d halos" % len(halo_list)
        else :
            return False

    profiles = read_halo_profiles(directory, aexp, halo_list = halo_list,
                                          profile_types = profile_types)

    add_remove_h_inverse(profiles, h_inverse, "in_profiles")

    return profiles

def read_halo_profiles(directory, aexp, filename_prefix = "halo_profile",
                       halo_list = [],
                       profile_types = ["gas", "mass", "velocity"]) :

    valid_profile_types = ["gas", "mass", "velocity"]
    for profile_type in profile_types :
        if profile_type not in valid_profile_types :
            sys.exit("profile type %s not recognized", profile_types)

    columns = {}
    
    filename = "%s/%s_%s_a%0.4f.dat" % (directory, filename_prefix,
                                                 profile_types[0], aexp)
    is_enabled_clump_exclusion = check_for_clump_exclusion(filename)

    columns["radius"] = ["r_in","r_mid","r_out","volume_bin", "volume"]

    # gas
    # gas_temperature(volume-weighted, mass-weighted) [K] 
    # gas_pressure(volume-weighted, mass-weighted) [ergs cm ^ {-3}] 
    # gas_entropy(volume-weighted, mass-weighted) [keV cm ^ 2]

    columns["gas"] = ["T_vw", "T_mw", "P_vw", "P_mw", "S_vw", "S_mw"]
        

    #mass
    # dark-M_(bin, cum) gas-M_(bin, cum) gas_cold-M_(bin, cum)
    # star-M_(bin, cum) star_new-M_(bin, cum) [M_sun/h]
    # dark-V_circ gas-V_circ star-V_circ total-V_circ [km/s physical]

    columns["mass"] = ["M_dark_bin", "M_dark", "M_gas_bin", "M_gas", 
                       "M_gas_cold_bin", "M_gas_cold", "M_star_bin",
                       "M_star", "M_star_new_bin", "M_star_new",
                       "vcirc_dark", "vcirc_gas", "vcirc_star", "vcirc_total"]

    if is_enabled_clump_exclusion :
        columns["mass"] += ["M_gas_bulk_bin", "M_gas_cold_bulk_bin",
                            "volume_bulk", "density_threshold"]
        
    # velocity
    # dark_V_ave dark_V_rad_(ave, std) dark_V_tan(ave, std)
    # gas-V_ave gas-V_rad_(ave, std) gas-V_tan_(ave, std)
    # gas_cold-V_ave gas_cold-V_rad_(ave, std) gas_cold-V_tan_(ave, std)
    # star-V_ave star-V_rad_(ave, std) star-V_tan_(ave, std) total-V_ave [km/s physical]

    columns["velocity"] = [ "vel_dark_avg", "vel_dark_rad_avg", "vel_dark_rad_std",
                            "vel_dark_tan_avg", "vel_dark_tan_std",
                            "vel_gas_avg", "vel_gas_rad_avg", "vel_gas_rad_std",
                            "vel_gas_tan_avg", "vel_gas_tan_std",
                            "vel_gas_cold_avg", "vel_gas_cold_rad_avg",
                            "vel_gas_cold_rad_std", 
                            "vel_gas_cold_tan_avg", "vel_gas_cold_tan_std",
                            "vel_star_avg", "vel_star_rad_avg", "vel_star_rad_std",
                            "vel_star_tan_avg", 
                            "vel_star_tan_std", "vel_total_avg"]

    radii_file = "%s/%s_radius_bin_a%0.4f.dat" % (directory, filename_prefix, aexp)
    radii, nrows = read_radii_profile_from_ascii(radii_file, columns["radius"])

    profiles = None
    
    logging.debug(halo_list)

    for profile_type in profile_types :
        filename = "%s/%s_%s_a%0.4f.dat" % (directory, filename_prefix,
                                                 profile_type, aexp)
        logging.debug(filename)

        profile = read_profile_from_ascii(filename, columns[profile_type],
                                          radii, halo_list = halo_list,
                                          nrows=nrows)

        if profiles is None :
            profiles = profile
        else :
            profiles = pd.merge(profiles, profile)

    profiles["aexp"] = aexp
#    return profiles.set_index(["id", "bin"])
    return profiles


def read_profile_from_ascii(filename, columns, radii, 
                            halo_list = None, nrows = None) :

    profiles = None
    i = 0

    with open(filename, 'r') as f:
        #read in header
        while 1 :
            line = f.readline()
            if line.startswith("##") :
                skiprows = i+2
                break

            if i == 0 and not nrows:
                #expects nrows to be last thing on first line
                nrows = int(line.split()[-1])
            i += 1

        while 1:
            line = f.readline()
            if not line : break

            if line.startswith("#") :

                halo_id = int(line.split()[1])

                if halo_list is None or halo_id in halo_list :
                    this_profile = pd.read_table(filename, sep=r"\s+", nrows=nrows, 
                                    skiprows=skiprows, names=columns)
                    this_profile = this_profile.join(radii)

                    this_profile["id"] = halo_id
                    
                    if profiles is None :
                        profiles = this_profile
                    else :
                        profiles = pd.concat([profiles,this_profile], ignore_index=True)
                        
                skiprows += nrows+1
    

    return profiles

def read_radii_profile_from_ascii(filename, columns) :

    i = 0
    with open(filename, 'r') as f:
        while 1 :
            line = f.readline()
            if not line.startswith("#") :
                skiprows = i
                break

            if i == 0:
                #expects nrows to be last thing on first line
                nrows = int(line.split()[-1])
            i += 1

    profile = pd.read_table(filename, sep=r"\s+", skiprows=skiprows, names=columns)
    profile["bin"] = np.arange(0,nrows)

    return profile, nrows

def read_halo_particles( filename,  min_np = 1000, clusters = None ):
    """
    loads particles (ids and binding energy) for halos
    from halo_particles_a*.dat files
    """

    if ( clusters != None ):
            cluster_hash = {}
            for c in clusters:
                    cluster_hash[c] = 1

    with open( filename, "r" ) as input :

        size=fromfile( input, dtype='i', count=1 )
        (aexpn,) = fromfile( input, dtype='f', count=1 )
        size=fromfile( input, dtype='i', count=1 )
        size=fromfile( input, dtype='i', count=1 )
        if size > 4+4:
            print "assuming long particle ids"
            particleid_t = 'int64'
        else:
            particleid_t = 'i'
        [nhd] = fromfile( input, dtype='i', count=1 )
        [np] = fromfile( input, dtype=particleid_t, count=1 )
        size=fromfile( input, dtype='i', count=1 )

        print 'ae,num_halos,np', aexpn, nhd, np

        cluster_data = {}

        for halo in xrange(nhd):
                size = fromfile( input, dtype='i', count=1 )
                [ih] = fromfile( input, dtype='i', count=1 )
                [inp] = fromfile( input, dtype='i', count=1 )

                if ih > nhd:
                        print halo, ih, nhd, 'quitting'
                        sys.exit()

                if halo % 1024 == 0:
                        print halo, "..."

                if ( clusters is None or cluster_hash.has_key(ih) ) and inp > min_np:

                    pids = fromfile( input, dtype=particleid_t, count=inp )
                    bind = fromfile( input, dtype='f', count=inp )

                    cluster_data[ih] = zip(pids,bind)
                    
                    #throw away radius
                    radius, = fromfile( input, dtype='i',count=1)

                else:
                    if particleid_t == 'i':
                        input.seek( 4*(2*inp+1), 1 )
                    else:
                        input.seek( 8*inp+4*inp+4*1, 1 )

    return cluster_data

def add_remove_h_inverse(halo_data, h_inverse, file_type) :

    if h_inverse[file_type] == h_inverse["into_db"] :
        logging.debug("h-1 status in ascii file matches database"
                      "request, no action taken")
        return
    elif h_inverse["into_db"] == True and h_inverse[file_type] == False :
        h_factor = h_inverse["h"]
    elif h_inverse["into_db"] == False and h_inverse[file_type] == True :
        h_factor = 1.0/h_inverse["h"]
    else :
        logging.error("Unregonized combo of h_inverse_into_db "
                      "and h_inverse_in_ascii set. Set these "
                      "settings to booleans.")

    for column in halo_data.columns.tolist() :
        if "M" in column :
            halo_data[column] *= h_factor
        elif column.startswith("r") :
            halo_data[column] *= h_factor
        elif "volume" in column :
            halo_data[column] *= (h_factor**3)

def check_for_clump_exclusion(filename) :
    '''
    Checks for clump exclusion keywords in file header. Pass
    mass profile file for best results.
    ''' 
    with open(filename, 'r') as f:
        #read in header
        while 1 :
            line = f.readline()
            if "clump density threshold" in line :
                cols = line.split()
                return cols[-1]

            if line.startswith("##") :
                return False
    

def comoving_physical_swap(halo_data, aexp, comoving_to_physical = True) :
    if comoving_to_physical :
        conversion = aexp
    else :
        conversion = 1.0/aexp

    for column in halo_data.columns.tolist() :
        if "M" in column :
            halo_data[column] *= conversion
        elif column.startswith("r") :
            halo_data[column] *= conversion

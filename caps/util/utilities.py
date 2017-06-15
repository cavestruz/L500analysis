#!/usr/bin/python

import sys
import logging

import numpy as np
import pandas as pd
import math

from math import pi, log, sqrt, fabs

from astropy.cosmology import WMAP5
#import cosmolopy.perturbation as cp

def define_axes(num_axes, vertical = False):

    if num_axes == 1:
        axis = [0.18, 0.16, 0.8, 0.8]

    elif num_axes == 1.5:

        axis = [ [0.16, 0.30, 0.80, 0.68],
                [0.16,0.16,0.8,0.14]]

    elif num_axes == 2.0:
        start = 0.09
        width = 0.4
        spacing = 0.007

        axis = [ [start,0.2,width,0.78],
            [start+spacing+width,0.2,width,0.78] ]

    elif num_axes == 3 and vertical == False:
        start = 0.09
        width = 0.28
        spacing = 0.007

        axis = [ [start,0.2,width,0.78],
            [start+spacing+width,0.2,width,0.78],
            [start+spacing*2+width*2,0.2,width,0.78] ]

    elif num_axes == 3  and vertical == True:

        start = 0.09
        width = 0.28
        spacing = 0.007

        axis = [ [0.2, start, 0.78, width],
            [0.2, start+spacing+width, 0.78, width],
            [0.2,start+spacing*2+width*2,0.78,width] ]

    else:
        sys.exit("axes for "+str(num_axes)+" `not yet defined")


    return axis

def compute_distance_periodic( pos_0,  pos_1, box_size):

    r = 0.0

    for d in range(3):
        dx = fabs( pos_0[d] - pos_1[d])

        if  dx > (box_size/2.0) :
            dx -= box_size;

        r += dx*dx;

    return sqrt(r);


def distance_between_halos(halo1, halo2, box_size):

    dx = compute_distance_periodic(
        [halo1["x"], halo1["y"], halo1["z"]],
        [halo2["x"], halo2["y"], halo2["z"]],
        box_size)

    return dx

def define_searchbox(halo, dt, boxsize, search_distance=1.0, radius="r_hc"):

    halo_pos = halo[["x","y","z"]].values
    halo_vel = halo[["vx","vy","vz"]].values

    search_radius = dt * math.sqrt(np.sum(np.square(halo_vel)))

    # convert km to Mpc (Note: need to account for h?)
    search_radius *= 3.24077929e-20
    search_radius += halo[radius]/1000.0
    search_radius *= search_distance

    logging.debug( "Search radius = %e Mpc/h" % (search_radius))

    searchbox = np.zeros(6)
    for d in range(3):
        x0 = halo_pos[d]-search_radius

        if x0 < 0: x0 += boxsize
        searchbox[(2*d)] = x0

        x1 = halo_pos[d]+search_radius
        if x1 >= boxsize: x1 -= boxsize
        searchbox[(2*d)+1] = x1

    return searchbox


def in_box(halo, searchbox):
    halo_pos = halo[["x","y","z"]].values

    for i in range(3):
        if searchbox[i*2] < searchbox[(i*2)+1]:
            if not (halo_pos[i] >= searchbox[i*2] and halo_pos[i] <= searchbox[(i*2)+1]):
                return False
        else:
            if not (halo_pos[i] <= searchbox[i*2] or halo_pos[i] >= searchbox[(i*2)+1]):
                return False

    return True

def reindex_and_interp(df, rbins=None, radius="200m"):
    if rbins is None :
        rbins = np.arange(0.1, 2, 0.05)

    radius = "r_vs_"+radius
    new_index = np.sort(np.concatenate((rbins, df[radius].values)))
    
    df = df.set_index([radius])
    df = df.reindex(new_index)
    df = df.interpolate(downcast=None)
    df = df.reindex(rbins)
    df[radius] = rbins

    return df

def calc_mass_accretion(sim, clusters_lowz, aexp="1.0005", aexp1="0.6503", radius="500c"):

    halo_data = sim.get_progenitor_properties(clusters_lowz, ["Mtotal_"+radius], aexp_list = [aexp, aexp1])

    lowz = halo_data[halo_data["aexp"] == aexp]
    highz = halo_data[halo_data["aexp"] == aexp1]

    halo_data = pd.merge(lowz, highz, on="z0_parent_id", suffixes=["", "_1"])

    halo_data["growth"] = halo_data["Mtotal_"+radius]/halo_data["Mtotal_"+radius+"_1"]

    growth = halo_data[["z0_parent_id","growth"]].copy()
    growth.rename(columns={"z0_parent_id":"id"}, inplace=True)

    return growth


def calc_gamma_accretion(sim, clusters_lowz, aexp=1.0005, aexp1=0.6503, radius="vir"):


    if radius != "vir":
        halo_data = sim.get_progenitor_properties(clusters_lowz, ["M_total_"+radius], aexp_list = [aexp, aexp1])

        lowz = halo_data[halo_data["aexp"] == aexp]
        highz = halo_data[halo_data["aexp"] == aexp1]

        halo_data = pd.merge(lowz, highz, on="z0_parent_id", suffixes=["", "_1"])

        halo_data["gamma"] = ( (np.log10(halo_data["M_total_"+radius]) - np.log10(halo_data["M_total_"+radius+"_1"]))/
                            (np.log10(halo_data["aexp"]) - np.log10(halo_data["aexp_1"])) )

        gamma = halo_data[["z0_parent_id","gamma"]].copy()
        gamma.rename(columns={"z0_parent_id":"id"}, inplace=True)

    else:
        print "vir radius not in database"

    return gamma

def calc_age_from_aexp(aexp):

   return WMAP5.age(1./float(aexp)-1).value


def load_tmerger_from_file(sim, dir, aexp=1.0):

    last_merger = sim.load_last_merger_epochs(dir,aexp)

    tmerger = {}

    for id in last_merger.keys():
        merger_z = (1./float(last_merger[id])-1)
        merger_time = WMAP5.age(merger_z)
        cosmic_age = WMAP5.age(1./float(aexp)-1)

#        merger_time = cosmocalc(merger_z)["zage_Gyr"]
#        cosmic_age = cosmocalc(1./float(aexp)-1)["zage_Gyr"]

        tmerger[id] = cosmic_age - merger_time

    return tmerger

def find_rvir_mvir(mass_profile, r_out, aexpn, overdensity = 200.0, crit = True, vir=False, omega_m=0.27, omega_l=0.73):
    """
    find rvir, mvir, and rho_vir given mass profile mtot, radial bins rr, expansion factor and overdensity with respect to critical (default) or mean (critical = False)
    """

    Ez = sqrt(omega_m/aexpn**3.0+omega_l)

    if crit or vir:
        rho_background = 2.775e2*Ez**2 # h^2Msun/kpc^3

    else:
        # this should be the mean density, not critical
        rho_background = omega_m* 2.775e2 /aexpn**3.0 # h^2Msun/kpc^3

        if vir:
            ## Use Bryan & Norman (1998) formula for virial overdensty wrt critical
            omega_z = omega_m/aexpn**3./Ez**2.
            overdensity = 18.0*pi*pi+82.0*(omega_z-1)-39.0*(omega_z-1)*(omega_z-1)

    rho_vir = overdensity * rho_background

    # this is the average density enclosed in radius rr in kpc/h
    sphvol = 4.0*pi/3.0*mass_profile**3.0
    rho_enc = np.log10(mass_profile/sphvol)
    lrr = np.log10(r_out)

    i = 0
    while rho_enc[i] > np.log10(rho_vir):
        i += 1

    # interpolate to find rvir
    rvir = 10.0**(lrr[i-1] + (lrr[i]-lrr[i-1])/(rho_enc[i]-rho_enc[i-1]) * (np.log10(rho_vir) - rho_enc[i-1]))
    mvir =  4.0*pi/3.0*rvir**3.0*rho_vir

    return rvir, mvir, rho_vir

def get_self_similar_temperature (halo, delta, crit=True, aexp=1.0):
    """
    Return self-similar quantites for temperature [keV] pressure [erg/cm^3], and entropy [keV cm^2] given halo mass mvir [Msun/h], its overdensity delta, with respect to critical (crit=True) or mean (crit=False) at expansion factor aexp (= 1.0 by default). Assume WMAP5 cosmological parameters (true for Bolshoi and L500 simulations).
    """

    from numpy import sqrt

    if crit :
        mvir = halo["M_total_"+str(delta)+"c"]
    else :
        mvir = halo["M_total_"+str(delta)+"m"]

    omega_m = 0.27
    omega_l = 0.73
    hubble = 0.7
    Ez = sqrt(omega_m/aexp**3.0+omega_l)
    mu = 0.59

    mpivot = 1e15 # in Msun/h

    delta = float(delta)

    if crit:
        Tfit_norm = 11.055*(mu/0.59)*(hubble/0.7)**(2./3.)
        Tfit_alpha = 2./3.
        Tfit_beta = 2./3.

        Tvir = (delta/500.0)**(1./3.)*Tfit_norm*(mvir/mpivot)**(Tfit_alpha)*Ez**(Tfit_beta)

    else:
        Tfit_norm = 5.2647*(mu/0.59)*(hubble/0.7)**(2./3.)*(omega_m/0.27)**(1./3.)
        Tfit_alpha = 2./3.
        Tfit_beta = -1.0

        Tvir = (delta/200.0)**(1./3.)*Tfit_norm*(mvir/mpivot)**(Tfit_alpha)*(aexp)**(Tfit_beta)


    return Tvir


def get_self_similar_pressure (halo, delta, crit=True, aexp=1.0):

    """
    Return self-similar quantites for temperature [keV] pressure [erg/cm^3], and entropy [keV cm^2] given halo mass mvir [Msun/h], its overdensity delta, with respect to critical (crit=True) or mean (crit=False) at expansion factor aexp (= 1.0 by default). Assume WMAP5 cosmological parameters (true for Bolshoi and L500 simulations).
    """

    from numpy import sqrt

    if crit :
        mvir = halo["M_total_"+str(delta)+"c"]
    else :
        mvir = halo["M_total_"+str(delta)+"m"]

    omega_m = 0.27
    omega_l = 0.73
    omega_b = 0.0469
    hubble = 0.7
    fb = omega_b/omega_m
    Ez = sqrt(omega_m/aexp**3.0+omega_l)

    mpivot = 1e15 # in Msun/h

    delta = float(delta)

    if crit:

        Pfit_norm = 1.4458e-11*(fb/0.1737)*(hubble/0.7)**2
        Pfit_alpha = 2./3.
        Pfit_beta = 8./3.

        Pvir = (delta/500.0)**(4./3.)*Pfit_norm*(mvir/mpivot)**(Pfit_alpha)*Ez**(Pfit_beta)
    else:

        Pfit_norm = 7.4359e-13*(fb/0.1737)*(hubble/0.7)**2*(omega_m/0.27)**(4./3.)
        Pfit_alpha = 2./3.
        Pfit_beta = 4.0

        Pvir = (delta/200.0)**(4./3.)*Pfit_norm*(mvir/mpivot)**(Pfit_alpha)/(aexp)**(Pfit_beta)

    return Pvir


def get_self_similar_entropy (halo, delta, crit=True, aexp=1.0):
    """
    Return self-similar quantites for temperature [keV] pressure [erg/cm^3], and entropy [keV cm^2] given halo mass mvir [Msun/h], its overdensity delta, with respect to critical (crit=True) or mean (crit=False) at expansion factor aexp (= 1.0 by default). Assume WMAP5 cosmological parameters (true for Bolshoi and L500 simulations).
    """

    from numpy import sqrt

    if crit :
        mvir = halo["M_total_"+str(delta)+"c"]
    else :
        mvir = halo["M_total_"+str(delta)+"m"]

    omega_m = 0.27
    omega_l = 0.73
    omega_b = 0.0469
    hubble = 0.7
    fb = omega_b/omega_m
    Ez = sqrt(omega_m/aexp**3.0+omega_l)
    mu = 0.59
    mue = 1.14

    mpivot = 1e15 # in Msun/h

    delta = float(delta)

    if crit:

        Kfit_alpha = 2./3.
        Kfit_beta = -2./3.
        Kfit_norm = 1963.6*(mu/0.59)*(mue/1.14)**(2./3.)*(fb/0.1737)**(-2./3.)*(hubble/0.7)**(-2./3.)

        Kvir = (delta/500.0)**(-1./3.)*Kfit_norm*(mvir/mpivot)**(Kfit_alpha)*Ez**(Kfit_beta)
    else:

        Kfit_alpha = 2./3.
        Kfit_beta = 1.0
        Kfit_norm = 4123.3*(mu/0.59)*(mue/1.14)**(2./3.)*(fb/0.1737)**(-2./3.)*(hubble/0.7)**(-2./3.)*(omega_m/0.27)**(-1./3.)

        Kvir = (delta/200.0)**(-1./3.)*Kfit_norm*(mvir/mpivot)**(Kfit_alpha)*(aexp)**(Kfit_beta)

    return Kvir



#def get_Mnl(z):
    """
    Return Mnl for a given redshift z.
    """

    #Cosmological Parameters for L500 and Bolshoi
#    cosmo = {'omega_M_0': 0.27, 'omega_lambda_0': 0.73, 'omega_b_0': 0.0469388, 'omega_n_0': 0.0, 'N_nu': 0,'h': 0.70, 'n': 0.96, 'sigma_8': 0.82, 'baryonic_effects': True}

#    omega_m = cosmo['omega_M_0']
#    omega_l = cosmo['omega_lambda_0']
#    omega_mz = omega_m*(1+z)**3
#    Ez = sqrt(omega_m*(1+z)**3.0+omega_l)
#    omega_z = omega_mz / (Ez*Ez)

    # mass bins in Msun/h
#    mbins = np.array(10**(np.arange(1,16,0.01)))
#    nu = np.zeros (len(mbins))

    # Build nu array
#    sigma = cp.sigma_r(cp.mass_to_radius(mbins/cosmo['h'], **cosmo), z, **cosmo)[0]
#    nu = 1.686/sigma

    # Compute Mnl which equals M when nu = 1
 #   closest = np.where(nu < 1.)[0][-1] #nu increases with M

    # Interplolate to get Mnl
#    Mnl = log10(mbins[closest]) + log10(mbins[closest+1]/mbins[closest])/log10(nu[closest+1]/nu[closest])*fabs(log10(nu[closest]))
#    Mnl = 10**Mnl

#    return Mnl

#def get_nu(mvir, z):
    """
    Return nu for a given halo mass Mvir and redshift z. Mvir is in Msun/h

    """

    #Cosmological Parameters for L500 and Bolshoi
#    cosmo = {'omega_M_0': 0.27, 'omega_lambda_0': 0.73, 'omega_b_0': 0.0469388, 'omega_n_0': 0.0, 'N_nu': 0,'h': 0.70, 'n': 0.96, 'sigma_8': 0.82, 'baryonic_effects': True}

   # omega_m = cosmo['omega_M_0']
   # omega_l = cosmo['omega_lambda_0']
    #omega_mz = omega_m*(1+z)**3
   # Ez = sqrt(omega_m*(1+z)**3.0+omega_l)
    #omega_z = omega_mz / (Ez*Ez)

#    sigma = cp.sigma_r(cp.mass_to_radius(mvir/cosmo['h'], **cosmo), z, **cosmo)[0]
#    nu = 1.686/sigma

#    return nu


### NOTE: concentration needs to be for delta_in
def convert_mass (M_in, delta_in, delta_out, aexp, concent = 5):
    # http://background.uchicago.edu/mass_convert/massconvert.f

    ratio = delta_in/delta_out

    fvalue = log(1.0+concent) - concent/(1+concent)
    fvalue = fvalue/ratio/concent**3.

    #convert mass
    M_out = M_in * ( (concent *convinv(fvalue))**-3./ratio)

    #convert concentration
    c_out = (convinv(fvalue)**-1.)

    return M_out, c_out

def convert_mass_factor(delta_in, delta_out, aexp, concent = 5, mean_to_crit = "same"):
    # mean_to_crit = "same": not changing density
    # mean_to_crit = "m_to_c": converting mean to critical
    # mean_to_crit = "c_to_m": converting critical to mean

    omega_m = 0.27*(1./aexp)**3
    omega_x0 = 0.73
    Ez2 = omega_m + omega_x0

    if mean_to_crit == "same":
        ratio = delta_in/delta_out
    elif mean_to_crit == "m_to_c":
        ratio = (delta_in/delta_out)/(Ez2/omega_m)
    elif mean_to_crit == "c_to_m":
        ratio = (delta_in/delta_out)*(Ez2/omega_m)
    else:
        print "unrecognized value for mean_to_crit"
        print '"same": not changing ref density, "m_to_c": converting mean to critical, "c_to_m": converting critical to mean'
        sys.exit()

    fvalue = log(1.0+concent) - concent/(1+concent)
    fvalue = fvalue/ratio/concent**3.

    #Mout/Min
    mass_ratio = ( (concent *convinv(fvalue))**-3./ratio)

    return mass_ratio


def convert_radius_to_vir(delta_in, aexp, concent = 5.):
    #assumes critical input at the moment

    omega_m = 0.27*(1./aexp)**3
    omega_x0 = 0.73
    Ez2 = omega_m + omega_x0
    x = omega_m - 1.
    delta_vir = (18.*pi**2. + 82.*x-39.*x**2.)/(1.+x)
  #  print delta_vir, omega_m
    ratio = delta_in/delta_vir*(Ez2/omega_m)
  #  print ratio
    fvalue = log(1.0+concent) - concent/(1.+concent)
    fvalue = fvalue/ratio/concent**3.

    return convinv(fvalue)*concent

def convert_radius_to_mean(delta_in, delta_out, aexp, concent = 5.):
    #assumes critical input at the moment

    omega_m = 0.27*(1./aexp)**3
    omega_x0 = 0.73
    Ez2 = omega_m + omega_x0
  #  print delta_vir, omega_m
    ratio = delta_in/delta_out*(Ez2/omega_m)
  #  print ratio
    fvalue = log(1.0+concent) - concent/(1.+concent)
    fvalue = fvalue/ratio/concent**3.

    return convinv(fvalue)*concent

def convert_radius_to_critical(delta_in, delta_out, aexp, concent = 5.):
    #assumes mean input at the moment

    omega_m = 0.27*(1./aexp)**3
    omega_x0 = 0.73
    Ez2 = omega_m + omega_x0
  #  print delta_vir, omega_m
    ratio = delta_in/delta_out/(Ez2/omega_m)
  #  print ratio
    fvalue = log(1.0+concent) - concent/(1.+concent)
    fvalue = fvalue/ratio/concent**3.

    return convinv(fvalue)*concent

def convinv(f):
    #fitting function from Hu & Kravtsov 2003

    a2 = 0.5116
    a3 = -1.285/3.
    a4 = -3.13e-3
    a5 = -3.52e-5

    p = a3 + a4*log(f) + a5*log(f)**2.
    convinv = a2*f**(2.*p) + (3./4.)**2.
    convinv = 1./sqrt(convinv) + 2.*f

    return convinv

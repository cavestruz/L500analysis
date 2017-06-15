#!/usr/bin/python

from config import *

### Should agree with column names in util/cart_io.py ###

def halo_catalog_units(radius) :
    h = "/h" if h_inverse["into_db"] else ""

    units = (
        ("aexp", "expansion factor", "", ""),
        ("id", "halo ID number", "", ""),
        ("x", "x location of halo center", "Mpc/h comoving", ""),
        ("y", "y location of halo center", "Mpc/h comoving", ""),
        ("z", "z location of halo center", "Mpc/h comoving", ""),
        ("vx", "peculiar velocity of halo in x direction", "km/s", ""),
        ("vy", "peculiar velocity of halo in y direction", "km/s", ""),
        ("vz", "peculiar velocity of halo in z direction", "km/s", ""),
        ("r_hc", "r from halo finder", "kpc"+h+" comoving", radius),
        ("M_hc", "M from halo finder", "Msun"+h, radius),
        ("num_particles", "number of particles", "", ""),
        ("vmax_hc", "maximum circular velocity from halo finder", "km/s", ""),
        ("rmax_hc", "maximum radius from halo finder",
         "kpc"+h+" comoving", ""),
        ("is_main_halo", "indicates if halo is a main halo", "", "")
    )

    return units


def halo_list_units(radii) :
    h = "/h" if h_inverse["into_db"] else ""

    units = []
    for radius in radii :
        units += (("r"+radius, "r"+radius+" radius","kpc"+h, ""),
               ("M_gas_"+radius, "mass of gas within r"+radius, "Msun"+h, ""),
               ("M_gas_cold_"+radius, "mass of cold gas within r"+radius, "Msun"+h, ""),
               ("M_star_"+radius, "stellar mass within r"+radius, "Msun"+h, ""),
               ("M_star_new_"+radius, "mass in new stars within r"+radius, "Msun"+h, ""),
               ("M_baryon_"+radius, "baryon mass within r"+radius, "Msun"+h, ""),
               ("M_dark_"+radius, "dark matter mass within r"+radius, "Msun"+h, ""),
               ("M_total_"+radius, "total mass within r"+radius, "Msun"+h, "")
               )

        if enabled_star_formation:
            units += (
                  ("gas-Z_II_avg_"+radius, "metallicity within r"+radius, "wrt solar", ""),
                  ("gas-Z_Ia_avg_"+radius, "metallicity within r"+radius, "wrt solar", ""),
                  ("star-Z_II_avg_"+radius, "metallicity within r"+radius, "wrt solar", ""),
                  ("star-Z_Ia_avg_"+radius, "metallicity within r"+radius, "wrt solar", ""),
                  ("star_new-Z_II_avg_"+radius, "metallicity within r"+radius, "wrt solar", ""),
                  ("star_new-Z_Ia_avg_"+radius, "metallicity within r"+radius, "wrt solar", ""),
                  ("star-age_avg_"+radius, "average stellar age within r"+radius, "Gyr", ""),
                  )

    return units

def profile_units() :

    h = "/h" if h_inverse["into_db"] else ""

    #mass and gas properties
    units = (
        ("r_in","radius of the middle of the bin","kpc"+h,""),
        ("r_mid","radius of the middle of the bin","kpc"+h,""),
        ("r_max","outer radius of the bin", "kpc"+h,""),
        ("volume","cumulative volume within r", "kpc physical ^ 3",""),
        ("M_dark","dark matter mass within r","Msun"+h,""),
        ("M_total","total mass within r","Msun"+h,""),
        ("density_total", "total density within r", "??", "WARNING: CLUMPS NOT REMOVED"),
        ("vcirc_dark","circular velocity of dark matter","km/s physical",""),
        ("vcirc_total","circular velocity of total matter","km/s physical","")
        )

    if enabled_hydro :
        units += (("M_gas","gas mass within r","Msun"+h,""),
                  ("M_gas_cold","cold gas mass within r","Msun"+h,""),
                  ("density_gas", "density of gas within r", "??","WARNING: CLUMPS NOT REMOVED"),
                  ("vcirc_gas","circular velocity of gas mass","km/s physical",""))

    if enabled_star_formation :
        units += (("M_star","stellar mass within r","Msun"+h,""),
                  ("M_star_new","new stellar mass within r","Msun"+h,""),
                  ("density_star", "density of stars within r", "??",""),
                  ("vcirc_gas","circular velocity of stars","km/s physical",""))

    #gas properties
    if enabled_hydro :

        units +=   (("T_vw","volume weighted temperature","K",""),
                    ("P_vw","volume weighted pressure","erg cm^{-3}",""),
                    ("S_vw","volume weighted entropy","keV cm^2",""),
                    ("T_mw","mass weighted entropy","keV cm^2",""),
                    ("P_mw","mass weighted entropy","keV cm^2",""),
                    ("S_mw","mass weighted entropy","keV cm^2",""),
                    ("P_rand","mass weighted non-thermal pressure due to random motions","keV cm^2","")
                    #("Ysz", "SZ Compton-Y", "Mpc^2","") ## WANT TO ADD THIS BACK
                    )

    #velocities
    units += (("vel_dark_avg","total dark matter velocity", "km/s physical", ""),
              ("vel_dark_rad_avg","average radial dark matter velocity", "km/s physical", ""),
              ("vel_dark_rad_std","std of radial dark matter velocity", "km/s physical", ""),
              ("vel_dark_tan_avg","average tangential dark matter velocity", "km/s physical", ""),
              ("vel_dark_tan_std","std of tangential dark matter velocity", "km/s physical", ""),
              ("vel_total_avg","average total velocity", "km/s physical", ""))

    if enabled_hydro :
        units += (("vel_gas_avg","total gas velocity", "km/s physical", ""),
                  ("vel_gas_rad_avg","average radial gas velocity", "km/s physical", ""),
                  ("vel_gas_rad_std","std of radial gas velocity", "km/s physical", ""),
                  ("vel_gas_tan_avg","average tangential gas velocity", "km/s physical", ""),
                  ("vel_gas_tan_std","std of tangential gas velocity", "km/s physical", ""))

    if enabled_star_formation :
        units += (("vel_star_avg","total star velocity", "km/s physical", ""),
                  ("vel_star_rad_avg","average radial star velocity", "km/s physical", ""),
                  ("vel_star_rad_std","std of radial star velocity", "km/s physical", ""),
                  ("vel_star_tan_avg","average tangential star velocity", "km/s physical", ""),
                  ("vel_star_tan_std","std of tangential star velocity", "km/s physical", ""))

    #electron properties
    if enabled_epnoneq :
            units += (("T_e", "electron temperature", "K",""),
                      ("Ysz_e", "SZ Compton-Y for electron pressure", "Mpc^2",""),
                      ("n_e", "electron number density","??",""),
                      ("t_ei", "??","??",""),
                      ("P_e", "electron pressure?","erg cm^{-3}",""))

    return units

def prand_units():

    units = (
            ("Ptherm", "thermal pressure","erg cm^{-3}",""),
            ("Prand", "pressure from random motions","erg cm^{-3}",""),
            ("Pmean", "pressure from mean gas motions", "erg cm^{-3}",""),
            ("rho_gas", "gas density in radial bin","g cm^{-3}",""),
            ("cs", "sound speed","km/s",""),
            ("v_r", "radial velocity","km/s",""),
            ("sig_r", "sigma radial","km/s",""),
            ("v_t", "tangential velocity","km/s",""),
            ("sig_t", "sigma tangential","km/s",""),
            ("sig_v", "sigma velocity", "km/s",""),
            ("Ptherm_cum", "cumulative thermal pressure","km/s",""),
            ("Prand_cum", "cumulative pressure from random motions","km/s",""),
            ("Pmean_cum", "cumulative pressure from mean motions","km/s",""),
            ("sum_dPthdrrho","dP/dr/(rho_gas)*dA thermal term from summation method", "erg g^-1 cm",""),
            ("sum_vr", "vrdvr/dr*dA from summation method", "km^3/s^2",""),
            ("sum_vtheta", "vtheta/r*dvr/(r*dtheta)*dA from summation method", "km^3/s^2",""),
            ("sum_vphi", "vphi/rsin(theta)*dvr/(r*sintheta*dphi)*dA from summation method", "km^3/s^2",""),
            ("sum_vrot2", "vrot^2*dA from summation method", "km^4/s^2",""),
            ("ave_vr", "vrdvr/dr from averaging method", "km/s^2",""),
            ("ave_vtheta", "vtheta/r*dvr/(r*dtheta) from averaging method", "km/s^2",""),
            ("ave_vphi", "vphi/rsin(theta)*dvr/(r*sintheta*dphi) from averaging method", "km/s^2",""),
            ("ave_dsig2dr", "dsig2dr from averaging method", "km/s^2",""),
            ("ave_dsig2dtheta", "dsig2dtheta from averaging method", "km/s^2",""),
            ("ave_dsig2dphi", "dsig2dphi from averaging method", "km/s^2",""),
            ("ave_sigrtheta2", "sigrtheta2 from averaging method", "km^2/s^2","")
            )

    return units


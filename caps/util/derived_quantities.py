#!/usr/bin/python

from astropy import units as u

def calc_prand(halo_data) :

    halo_data["sigv2"] = (halo_data["vel_gas_rad_std"]**2 
                          + halo_data["vel_gas_tan_std"]**2 )

    if "rho_gas_bulk" not in halo_data.columns :
        if "volume_bulk" in halo_data.columns :
            calc_density(halo_data, "gas_bulk")
            halo_data["P_rand"] = halo_data["rho_gas_bulk_bin"] * 1/3.* halo_data["sigv2"]
        else :
            calc_density(halo_data, "gas")
            halo_data["P_rand"] = halo_data["rho_gas_bin"] * 1/3.* halo_data["sigv2"]


    #units from (km/s)^2 * g * cm ^ {-3} to ergs cm ^ {-3}
    halo_data["P_rand"] *= (1e5)**2


def calc_all_densities(halo_data, h_inverse = True, h = 0.7) :

    calc_density(halo_data, "gas", h_inverse=h_inverse, h=h)
    calc_density(halo_data, "dark", h_inverse=h_inverse, h=h)
    calc_density(halo_data, "star", h_inverse=h_inverse, h=h)

    halo_data["rho_baryon"] = halo_data["rho_gas"] + halo_data["rho_gas"]

    halo_data["rho_total"] = halo_data["rho_baryon"] + halo_data["rho_dark"]

    if "rho_gas_bulk" not in halo_data.columns and "volume_bulk" in halo_data.columns:
        calc_density(halo_data, "gas_bulk")

def calc_density(halo_data, type, h_inverse = True, h = 0.7) :
    
    g_cm3 = u.g/(u.cm*u.cm*u.cm)
    Msun_kpc3 = (u.M_sun)/(u.kpc*u.kpc*u.kpc)
    conversion = Msun_kpc3.to(g_cm3)

    if h_inverse :
         conversion *= h*h

    halo_data["rho_"+type+"_bin"] = halo_data["M_"+type+"_bin"]/halo_data["volume_bin"]
    if "bulk" not in type:
        halo_data["rho_"+type] = halo_data["M_"+type]/halo_data["volume"]
        halo_data["rho_"+type] *= conversion

    halo_data["rho_"+type+"_bin"] *= conversion

def calc_total_mass(halo_data) :

    halo_data["M_total_bin"] = (halo_data["M_gas_bin"]
                                + halo_data["M_star_bin"]
                                + halo_data["M_dark_bin"])

    halo_data["M_total"] = (halo_data["M_gas"]
                            + halo_data["M_star"]
                            + halo_data["M_dark"])







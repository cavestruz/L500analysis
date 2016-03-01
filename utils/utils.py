import numpy as np
import constants as const

def match_nearest(estimates=None, exactvals=None): 
    '''Output the closest values from arg2 to arg1'''
    
    return [ min(exactvals, key=lambda x : abs(float(x)-float(estimate)))
             for estimate in estimates ]


def aexp2redshift(aexp=None) :
    '''Redshift conversion, no redshifts above below 0'''

    return max(1./float(aexp) - 1, 0.0)

def calculate_Ez(aexp=None,redshift=None,
                 OmM=const.omega_m,
                 OmL=const.omega_l) :
    '''Hubble expansion'''

    if redshift == None : redshift = aexp2redshift(aexp)

    return np.sqrt(OmM*float(1.+redshift)**3+OmL)


def calculate_rhoc(aexp=None,
                   OmM=const.omega_m,
                   OmL=const.omega_l) :

    Ez = calculate_Ez(aexp, OmM, OmL)

    return const.rhoc_0 * Ez**2

def calculate_rhom(aexp=None, 
                   OmM=const.omega_m) :
    
    return const.rho_0 * OmM / aexp**3

def calculate_Omz(aexp=None,OmM=const.omega_m,
                  OmL=const.omega_l) :

    Ez = calculate_Ez(aexp=aexp,OmM=OmM,OmL=OmL)
    return OmM/aexp**3/Ez**2.

def calculate_bryannorman98_overdensity(Omz=None) :

    return 18.0*np.pi**2+82.0*(Omz-1)-39.0*(Omz-1)**2

def K2keV(TinKelvin=None) :
    return TinKelvin*const.kb

'''
Functions to calculate virial properties, integrated properties, etc.
'''

import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *

def calculate_virial_mass(radii_kpc_h=None, M_tot=None,
                          aexp=None, delta=None) :
    
    cutoff_density = _calculate_cutoff_background_density(delta=delta,aexp=aexp)
    


def calculate_virial_radius(radii_kpc_h=None, M_tot=None,
                          aexp=None, delta=None) :
    cutoff_density = _calculate_cutoff_background_density(delta=delta,aexp=aexp)

    calculate_enclosed_density( radii_kpc_h=radii_kpc_h,
                                M_tot=None )

def calculate_enclosed_density() :
    pass

def interpolate_profile() :
    pass

def _calculate_cutoff_background_density(delta=None,aexp=None) :
    '''Calculates cutoff background density in h^2Msun/kpc^3'''
    
    overdensity_type = {'c':calculate_rhoc(aexp=aexp),
                        'm':calculate_rhom(aexp=aexp)}

    if delta=='bryan_norman98' :
        overdensity = calculate_bryan_norman98_overdensity(
            Omz=calculate_Omz(aexp=aexp))

        return overdensity*overdensity_type['c']

    else : 
        overdensity = float(delta[:-1])
        return overdensity*overdensity_type[delta[-1]]



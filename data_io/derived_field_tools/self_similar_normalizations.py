import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *

def calculate_T_normalization_wrt_critical(Mvir=None, delta=500, aexp=None,
                   OmM=constants.omega_m, OmL=constants.omega_l,
                   hubble=constants.hubble) :
    '''
    Returns self similar value of temperature in keV with respect to
    overdensity $\delta_{critical}$.
    '''

    self_similar_normalization_input = {
            'overdensity_ratio': delta/500.,
            'overdensity_power': 1./3,
            'normalization_fit': 11.055*(constants.mu/0.59)*(hubble/0.7)**(2./3.),
            'mass_1e15': Mvir/1e15,
            'mass_power': 2./3,
            'redshift_dependence': calculate_Ez(aexp=aexp, OmM=OmM, OmL=OmL),
            'redshift_dependence_power': 2./3
            }

    return self_similar_normalization(**self_similar_normalization_input)


def calculate_T_normalization_wrt_mean(Mvir=None, delta=200, aexp=None,
                   OmM=constants.omega_m, OmL=constants.omega_l,
                   hubble=constants.hubble) :
    '''
    Returns self similar value of temperature in keV with respect to
    overdensity $\delta_{mean}$.
    '''

    self_similar_normalization_input = {
            'overdensity_ratio': delta/200.,
            'overdensity_power': 1./3,
            'normalization_fit': 5.2647*(mu/0.59)*(hubble/0.7)**(2./3.)*(OmM/0.27)**(1./3.),
            'mass_1e15': Mvir/1e15,
            'mass_power': 2./3,
            'redshift_dependence': aexp,
            'redshift_dependence_power': -1.
            }

    return self_similar_normalization(**self_similar_normalization_input)





def self_similar_normalization(overdensity_ratio=None,
                               overdensity_power=None,
                               normalization_fit=None,
                               mass_1e15=None,
                               mass_power=None,
                               redshift_dependence=None,
                               redshift_dependence_power=None) :
    '''
    General calculation for self-similar normalization for thermodynamic variables
    '''

    return overdensity_ratio**overdensity_power * \
        normalization_fit * \
        mass_1e15 ** mass_power * \
        redshift_dependence ** redshift_dependence_power
        

import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *

def _self_similar_normalization(overdensity_ratio=None,
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

def calculate_T_normalization(Mvir=None, aexp=None, delta=None,
                   OmM=constants.omega_m, OmL=constants.omega_l,
                   hubble=constants.hubble, **kwargs) :
    '''
    Returns self similar value of temperature in keV with respect to
    overdensity $\delta_{critical}$ or $\delta_{mean}$ 
    kwargs 
    ---------
    delta: '200m', '500c', etc.
    '''
    
    delta_type = delta[-1]
    delta_value = float(delta[:-1])

    self_similar_normalization_input_crit = {
            'overdensity_ratio': delta_value/500,
            'overdensity_power': 1./3,
            'normalization_fit': 11.055*(constants.mu/0.59)*(hubble/0.7)**(2./3.),
            'mass_1e15': Mvir/1e15,
            'mass_power': 2./3,
            'redshift_dependence': calculate_Ez(aexp=aexp, OmM=OmM, OmL=OmL),
            'redshift_dependence_power': 2./3
            }

    self_similar_normalization_input_mean = {
            'overdensity_ratio': delta_value/200,
            'overdensity_power': 1./3,
            'normalization_fit': 5.2647*(constants.mu/0.59)*(constants.hubble/0.7)**(2./3.)*(OmM/0.27)**(1./3.),
            'mass_1e15': Mvir/1e15,
            'mass_power': 2./3,
            'redshift_dependence': aexp,
            'redshift_dependence_power': -1.
            }
    
    self_similar_normalization_input = {'c':self_similar_normalization_input_crit,
                                        'm':self_similar_normalization_input_mean
                                            }
                                            
    return _self_similar_normalization(**self_similar_normalization_input[delta_type])


def calculate_S_normalization(Mvir=None, aexp=None, delta=None,
                   OmM=constants.omega_m, OmL=constants.omega_l,
                   hubble=constants.hubble, **kwargs) :
    '''
    Returns self similar value of temperature in keV cm^2 with respect to
    overdensity $\delta_{critical}$ or $\delta_{mean}$ 

    kwargs 
    ---------
    delta: '200m', '500c', etc.
    '''
    
    delta_type = delta[-1]
    delta_value = float(delta[:-1])

    self_similar_normalization_input_crit = {
            'overdensity_ratio': delta_value/500,
            'overdensity_power': -1./3,
            'normalization_fit': 1265.7*(constants.mu/0.59)**(5./3)*\
                (constants.fb/.1737*constants.hubble/0.7)**(-2./3.),
            'mass_1e15': Mvir/1e15,
            'mass_power': 2./3,
            'redshift_dependence': calculate_Ez(aexp=aexp, OmM=OmM, OmL=OmL),
            'redshift_dependence_power': -2./3
            }

    self_similar_normalization_input_mean = {
            'overdensity_ratio': delta_value/200,
            'overdensity_power': 4./3,
            'normalization_fit': 2799.75*(constants.mu/0.59)**(5./3)\
                *(constants.fb/.1737*constants.hubble/0.7)**(-2./3.)\
                *(OmM/0.27)**(-1./3.),
            'mass_1e15': Mvir/1e15,
            'mass_power': 2./3,
            'redshift_dependence': aexp,
            'redshift_dependence_power': 1.
            }
    
    self_similar_normalization_input = {'c':self_similar_normalization_input_crit,
                                        'm':self_similar_normalization_input_mean
                                            }
                                            
    return _self_similar_normalization(**self_similar_normalization_input[delta_type])



def calculate_rho_normalization(aexp=None, delta=None,
                                OmM=constants.omega_m,
                                OmL=constants.omega_l,
                                **kwargs) :
    ''' 
    Returns self similar value of density in g/cm^3
    respect to overdensity $\delta_{critical}$ or $\delta_{mean}$
 
    kwargs 
    --------- 
    delta: '200m', '500c', etc.
    '''

    delta_type = delta[-1]
    delta_value = float(delta[:-1])

    self_similar_normalization_input_crit = {
        'overdensity_ratio': delta_value,
        'overdensity_power': 1.,
        'normalization_fit': 2.775e2,
        'mass_1e15': 1.,
        'mass_power': 1.,
        'redshift_dependence': calculate_Ez(aexp=aexp, OmM=OmM, OmL=OmL),
        'redshift_dependence_power': 2.
        }

    self_similar_normalization_input_mean = {
        'overdensity_ratio': delta_value,
        'overdensity_power': 1.,
        'normalization_fit': 2.775e2*OmM,
        'mass_1e15': 1.,
        'mass_power': 1.,
        'redshift_dependence': aexp,
        'redshift_dependence_power': -3.
        }
    
    self_similar_normalization_input = {'c':self_similar_normalization_input_crit,
                                        'm':self_similar_normalization_input_mean
                                            }

    return _self_similar_normalization(**self_similar_normalization_input[delta_type])

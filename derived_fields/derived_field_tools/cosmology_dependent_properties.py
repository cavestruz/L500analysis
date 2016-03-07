import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *
import cosmolopy.perturbation as cp

def _get_cosmology(omega_M_0=constants.omega_m, omega_lambda_0=constants.omega_l,
                  omega_b_0=constants.omega_b, omega_n_0=0.0, N_nu=0,
                  h=constants.hubble, n=constants.power_spectrum_index_n,
                  sigma_8=constants.sigma_8, baryonic_effects=True) :
    
    return locals()


def calculate_peak_height(Mvir=None, redshift=None,aexp=None,
                          cosmology=_get_cosmology()) :

    redshift = check_redshift_kwargs(redshift=redshift,aexp=aexp)

    mass2radius = cp.mass_to_radius(Mvir/cosmology['h'], **cosmology)
    
    sigma_m = cp.sigma_r( mass2radius, redshift, **cosmology)[0]

    return constants.delta_c / sigma_m
    

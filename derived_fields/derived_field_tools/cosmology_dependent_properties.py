import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *
import cosmolopy.perturbation as cp
import cosmolopy.density as cdens
import cosmolopy.distance as cdist

def _get_cosmology(omega_M_0=constants.omega_m, omega_lambda_0=constants.omega_l,
                  omega_b_0=constants.omega_b, omega_n_0=0.0, N_nu=0, omega_k_0=0,
                  h=constants.hubble, n=constants.power_spectrum_index_n,
                  sigma_8=constants.sigma_8, baryonic_effects=True) :
    
    return locals()


def calculate_peak_height(Mvir=None, redshift=None,aexp=None,
                          cosmology=_get_cosmology()) :

    redshift = check_redshift_kwargs(redshift=redshift,aexp=aexp)

    mass2radius = cp.mass_to_radius(Mvir/cosmology['h'], **cosmology)
    
    sigma_m = cp.sigma_r( mass2radius, redshift, **cosmology)[0]

    return constants.delta_c / sigma_m
    
def calculate_rhoc_cosmopy(redshift=None, aexp=None,
                   cosmology=_get_cosmology()) :
    pass

    redshift = check_redshift_kwargs(redshift=redshift,aexp=aexp)

    H_z = cdist.hubble_z(redshift, **cosmology) # /s

    assert(3.*H_z**2/(8.*np.pi*constants.gravc) == \
               cdens.cosmo_densities(**cosmology)[0]*cdist.e_z(redshift,**cosmology)**2) 

    return 3.*H_z**2/(8.*np.pi*constants.gravc)

def calculate_rhom_cosmopy(redshift=None, aexp=None,
                   cosmology=_get_cosmology()) :
    pass
    redshift = check_redshift_kwargs(redshift=redshift,aexp=aexp)

    OmM_z = cdens.omega_M_z(redshift,**cosmology)

    assert( OmM_z*calculate_rhoc_cosmopy(redshift=redshift, aexp=aexp, **cosmology) == cdens.cosmo_densities(**cosmology[0])*(1-redshift)**3. )

    return OmM_z*calculate_rhoc_cosmopy(redshift=redshift, aexp=aexp, **cosmology) 

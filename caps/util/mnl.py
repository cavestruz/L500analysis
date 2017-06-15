from numpy import *
from scipy import *
import cosmolopy.perturbation as cp

def getMnl(z) :
    """
    Return Mnl for a given redshift z.
    """

    #Cosmological Parameters for L500 and Bolshoi
    cosmo = {'omega_M_0' : 0.27, 'omega_lambda_0' : 0.73, 'omega_b_0' : 0.0469388, 'omega_n_0' : 0.0, 'N_nu' : 0,'h' : 0.70, 'n' : 0.96, 'sigma_8' : 0.82, 'baryonic_effects': True}
    
    omega_m = cosmo['omega_M_0']
    omega_l = cosmo['omega_lambda_0']
    omega_mz = omega_m*(1+z)**3
    Ez = sqrt(omega_m*(1+z)**3.0+omega_l)
    omega_z = omega_mz / (Ez*Ez)

    # mass bins in Msun/h
    mbins = array(10**(arange(1,16,0.01)))
    nu = zeros (len(mbins))

    # Build nu array
    sigma = cp.sigma_r(cp.mass_to_radius(mbins/cosmo['h'], **cosmo), z, **cosmo)[0]
    nu = 1.686/sigma

    # Compute Mnl which equals M when nu = 1
    closest = where(nu < 1.)[0][-1] #nu increases with M

    # Interplolate to get Mnl
    Mnl = log10(mbins[closest]) + log10(mbins[closest+1]/mbins[closest])/log10(nu[closest+1]/nu[closest])*fabs(log10(nu[closest]))
    Mnl = 10**Mnl

    return Mnl

def getnu(mvir,z) :
    """
    Return nu for a given halo mass Mvir and redshift z. Mvir is in Msun/h

    """

    #Cosmological Parameters for L500 and Bolshoi
    cosmo = {'omega_M_0' : 0.27, 'omega_lambda_0' : 0.73, 'omega_b_0' : 0.0469388, 'omega_n_0' : 0.0, 'N_nu' : 0,'h' : 0.70, 'n' : 0.96, 'sigma_8' : 0.82, 'baryonic_effects': True}
    
    omega_m = cosmo['omega_M_0']
    omega_l = cosmo['omega_lambda_0']
    omega_mz = omega_m*(1+z)**3
    Ez = sqrt(omega_m*(1+z)**3.0+omega_l)
    omega_z = omega_mz / (Ez*Ez)

    sigma = cp.sigma_r(cp.mass_to_radius(mvir/cosmo['h'], **cosmo), z, **cosmo)[0]
    nu = 1.686/sigma

    return nu


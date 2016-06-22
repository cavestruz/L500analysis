'''
Functions to calculate virial properties, integrated properties, etc.
'''
import numpy as np
import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *
import L500analysis.plotting.profiles.tools.make_profile as mp
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_T_normalization

class CalculateHaloProperties :
    def __init__( self, 
                  physical_radial_profile=None, mass_enclosed_profile=None,
                  delta=None,aexp=None) :
        '''
        Expects physical radial profile in kpc/h and mass enclosed in Msun/h.
        delta should be of form 200c, 200m, etc. OR "bryan_norman98"   
        '''

        self.delta=delta
        self.aexp=aexp
        self._test_profiles(physical_radial_profile, mass_enclosed_profile)
        self._calculate_interpolated_enclosed_density(physical_radial_profile=physical_radial_profile,
                                                      mass_enclosed_profile=mass_enclosed_profile)
        self._calculate_cutoff_density()
        self._get_virial_indices()

    def _test_profiles(self,physical_radial_profile,mass_enclosed_profile) :
        try :
            assert( len(physical_radial_profile) == len(mass_enclosed_profile) )
        except : 
            print physical_radial_profile
            print mass_enclosed_profile
            raise AssertionError('unequal length profiles, cannot calculate halo property')


    def _calculate_cutoff_density(self) :
        self.cutoff_density = calculate_cutoff_background_density(delta=self.delta, aexp=self.aexp)

    def _calculate_interpolated_enclosed_density(self,
                                    physical_radial_profile=None,
                                    mass_enclosed_profile=None) :

        self.interpolated_radius = constants.linear_rbins
        self.interpolated_mass_enclosed = mp.make_profile_linear(profile_rbins=constants.linear_rbins,x=physical_radial_profile,y=mass_enclosed_profile)
        self.interpolated_enclosed_density = self.interpolated_mass_enclosed / (4./3. * np.pi * self.interpolated_radius**3)

    def _get_virial_indices(self) :
        self.virial_indices = np.where(self.interpolated_enclosed_density>self.cutoff_density)[-1][-1]

    def calculate_virial_mass(self) :
        ''' In Msun/h '''
        return self.interpolated_mass_enclosed[self.virial_indices]*constants.hubble

    def calculate_virial_radius(self) :
        '''In kpc/h '''
        return self.interpolated_radius[self.virial_indices]*constants.hubble

    def calculate_virial_temperature(self) :
        '''T delta in keV, expects Mvir in Msun/h'''
        return calculate_T_normalization(Mvir=self.calculate_virial_mass(),
                                         aexp=self.aexp,
                                         delta=self.delta)
    def print_virial_indices(self) :
        print self.virial_indices

def calculate_cutoff_background_density(delta=None,aexp=None) :
    '''Calculates cutoff background density in Msun/kpc^3'''
    
    overdensity_type = {'c':calculate_rhoc(aexp=aexp),
                        'm':calculate_rhom(aexp=aexp)}
    
    if delta=='bryan_norman98' :
        overdensity = calculate_bryan_norman98_overdensity(
            Omz=calculate_Omz(aexp=aexp))
        
        return overdensity*overdensity_type['c']*\
            constants.g2Msun/constants.cm2kpc**3 
    
    else : 
        overdensity = float(delta[:-1])
        return overdensity*overdensity_type[delta[-1]]\
            *constants.g2Msun/constants.cm2kpc**3
    



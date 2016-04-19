'''
Functions to calculate virial properties, integrated properties, etc.
'''
import numpy as np
import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *
from L500analysis.plotting.profiles.tools.make_profile import make_profile_linear 
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
        self._calculate_interpolated_enclosed_density(physical_radial_profile=physical_radial_profile,
                                                      mass_enclosed_profile=mass_enclosed_profile)
        self._calculate_cutoff_density()
        self._get_virial_indices()

    def _calculate_cutoff_density(self) :
        self.cutoff_density = calculate_cutoff_background_density(delta=self.delta, aexp=self.aexp)

    def _calculate_enclosed_density(self,
                                    physical_radial_profile=None,
                                    mass_enclosed_profile=None) :
        self.interpolated_radius = make_profile_linear(x=physical_radial_profile,y=physical_radial_profile)
        self.interpolated_mass_enclosed = make_profile_linear(x=physical_radial_profile,y=mass_enclosed_profile)
        self.interpolated_enclosed_density = interpolated_mass_enclosed / (4./3. * pi * interpolated_radius**3)

    def _get_virial_indices(self) :
        self.virial_indices = np.where(self.interpolated_enclosed_density<self.cutoff_density \
                                           and self.interpolated_enclosed_density>self.cutoff_density)

    def calculate_virial_mass(self) :
        return self.interpolated_mass_enclosed(virial_indices)

    def calculate_virial_radius(self) :
        return self.interpolated_radius(virial_indices)

    def calculate_virial_temperature(self) :
        '''T delta in keV, expects Mvir in Msun/h'''
        return calculate_T_normalization(Mvir=self.calculate_virial_mass(),
                                         aexp=self.aexp,
                                         delta=self.delta)


def calculate_cutoff_background_density(delta=None,aexp=None) :
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



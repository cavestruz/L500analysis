from L500analysis.data_io.derived_fields import *
from L500analysis.data_io.derived_field_functions import *


def _r500c_profile(data,*args,**kwargs) :

    return {'profile':data.profiles['r_mid'], 
            'normalization':data.halo_properties['r500c']}

def _total_halo_mass(data, *args, **kwargs) :

    return data.profiles['M_dark'], data.profiles['M_star'], data.profiles['M_gas'] 



add_derived_field('M_tot',function=_total_halo_mass,
                  combine_function=sum_profiles)
add_derived_field('R/R500c',function=_r500c_profile,
                  combine_function=normalize_profile,
                  )

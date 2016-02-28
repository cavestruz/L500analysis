from L500analysis.data_io.derived_fields import *
from L500analysis.data_io.derived_field_functions import *
from L500analysis.data_io.derived_field_tools import *


def _r500c_normalization(data,*args,**kwargs) :

    return {'profile':data.profiles['r_mid'], 
            'normalization':data.halo_properties['r500c']}

def _nomalized_non_thermal_temperature(data, *args, **kwargs) :
    pass

def _normalized_total_temperature_profile(data, *args, **kwargs) :
    
    T_mw = data.profiles['T_mw']
    sigr=data.profiles['vel_gas_rad_std']
    sigt=data.profiles['vel_gas_tan_std']
    vr = data.profiles['vel_gas_rad_avg']
    vt = data.profiles['vel_gas_tan_avg']
    Mvir = data.profiles['']
    return {'sigr':sigr, 'sigt':sigt, 'vr':vr, 'vt':vt, 
            'T_mw':T_mw, 'aexp': data.aexp, 'Mvir': }

def calculate_normalized_nonthermal_temperature_profile(input_data) :
    # Note, can feed in a concatenated dictionary: dict(dic1, **dic2)
    # calculate_self_similar... quantities requires Mvir calculation first!
    # 
    d = input_data
    pass

def calculate_normalized_total_temperature_profile(input_data) :

    # Note, can feed in a concatenated dictionary: dict(dic1, **dic2)
    # calculate_self_similar... quantities requires Mvir calculation first!
    # 

    d = input_data
    T_tot_normalized = {}

    for hid in d['halo_ids'] :
        T_tot_normalized[hid] = d['T_mw']*constants.kb
        T_tot_normalized[hid] += 
    
    return T_tot_normalized


add_derived_field('T_tot',function=_total_temperature_profile,
                  combine_function=calculate_total_temperature)
add_derived_field('R/R500c',function=_r500c_normalization,
                  combine_function=normalize_profile,
                  )

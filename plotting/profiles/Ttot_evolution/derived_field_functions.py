import L500analysis.data_io as dio
from dio.derived_fields import *
from dio.derived_field_functions import *
from dio.derived_field_tools.non_thermal_temperature \
    import calculate_T_nonthermal
from dio.derived_filed_tools.integrated_halo_properties \
    import calculate_virial_mass
from dio.derived_filed_tools.self_similar_normalizations \
    import calculate_T_normalization_wrt_critical

def _r500c_normalization(data,*args,**kwargs) :

    return {'profile':data.profiles['r_mid'], 
            'normalization':data.halo_properties['r500c']}

def _nomalized_non_thermal_temperature(data, *args, **kwargs) :
    pass

    T_mw = data.profiles['T_mw']
    sigr=data.profiles['vel_gas_rad_std']
    sigt=data.profiles['vel_gas_tan_std']
    vr = data.profiles['vel_gas_rad_avg']
    vt = data.profiles['vel_gas_tan_avg']
    return { 'sigr':sigr, 'sigt':sigt, 'vr':vr, 'vt':vt, 
            'T_mw':T_mw, 'aexp': data.aexp }

def _normalized_total_temperature_profile(data, *args, **kwargs) :
    
    return data

def calculate_normalized_nonthermal_temperature_profile(input_data) :
    # Note, can feed in a concatenated dictionary: dict(dic1, **dic2)
    # calculate_self_similar... quantities requires Mvir calculation first!
    # need to use calculate_T_nonthermal
    sigr='vel_gas_rad_std'
    sigt='vel_gas_tan_std'
    vr='vel_gas_rad_avg'
    vt='vel_gas_tan_std'
    rmid='rmid'
    d = input_data

    for hid in d.halo_ids :
        Tnt = calculate_T_nonthermal(sigr=d[sigr][hid],vr=d[vr][hid],
                                     sigt=d[sigt][hid],vt=d[vt][hid])
        Mvir = calculate_virial_mass(radii_kpc=d[r_mid][hid], M_tot=None,
                          aexp=d['aexp'], delta=None)
        T500c = calculate_T_normalization_wrt_critical(Mvir=Mvir,
                                                       delta=500,
                                                       aexp=d['aexp'])
        


def calculate_normalized_total_temperature_profile(input_data) :

    # Note, can feed in a concatenated dictionary: dict(dic1, **dic2)
    # calculate_self_similar... quantities requires Mvir calculation first!
    # 

    d = input_data
    T_tot_normalized = {}

    for hid in d['halo_ids'] :
        d_halo = {key: d
        T_tot_normalized[hid] = d['T_mw']*constants.kb
        T_tot_normalized[hid] += 
    
    return T_tot_normalized


add_derived_field('T_tot',function=_total_temperature_profile,
                  combine_function=calculate_total_temperature)
add_derived_field('R/R500c',function=_r500c_normalization,
                  combine_function=normalize_profile,
                  )

from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.derived_fields.derived_field_tools.non_thermal_temperature \
    import calculate_T_nonthermal, calculate_Ttot
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_T_normalization

def _radial_normalization(data,*args,**kwargs) :

    r_delta = kwargs['r_delta']

    return {'profile':data.profiles['r_mid'], 
            'normalization':data.halo_properties[r_delta]}

def _normalized_total_temperature_profile(data, *args, **kwargs) :

    T_mw = data.profiles['T_mw']
    Mvir = data.halo_properties[kwargs['M_delta']]
    sigr=data.profiles['vel_gas_rad_std']
    sigt=data.profiles['vel_gas_tan_std']
    vr = data.profiles['vel_gas_rad_avg']
    vt = data.profiles['vel_gas_tan_avg']

    return dict({ 'sigr':sigr, 'sigt':sigt, 'vr':vr, 'vt':vt, 
                  'aexp':data.aexp, 'Mvir':Mvir, 'T_mw':T_mw,
                  'halo_ids':data.halo_ids }, **kwargs)

def calculate_normalized_nonthermal_temperature_profile(input_data) :

    d = input_data
    normalized_Tnt = {}
    for hid in d['halo_ids'] :
        Tnt = calculate_T_nonthermal(sigr=d['sigr'][hid],vr=d['vr'][hid],
                                     sigt=d['sigt'][hid],vt=d['vt'][hid])

        Tdelta = calculate_T_normalization(Mvir=d['Mvir'][hid],
                                          delta=d['delta'],
                                          aexp=d['aexp'])

        normalized_Tnt[hid] = Tnt/Tdelta

    return normalized_Tnt


def calculate_normalized_total_temperature_profile(input_data) :

    d = input_data
    T_tot_normalized = {}

    for hid in d['halo_ids'] :
        Tdelta = calculate_T_normalization(Mvir=d['Mvir'][hid],
                                          delta=d['delta'],
                                          aexp=d['aexp'])

        Ttot = calculate_Ttot(sigr=d['sigr'][hid],vr=d['vr'][hid],
                                      sigt=d['sigt'][hid],vt=d['vt'][hid],
                                      Tmw=d['T_mw'][hid])

        T_tot_normalized[hid] = Ttot/Tdelta
    
    return T_tot_normalized


add_derived_field('R/R500c',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r500c'
                  )

#add_derived_field('T_mw/T500c',function=_temperature_normalization,
#                  combine_function=self_similar_normalization, delta='500c')

add_derived_field('Tnt/T500c',function=_normalized_total_temperature_profile,
                  combine_function=calculate_normalized_nonthermal_temperature_profile
                  , M_delta='M_total_500c',delta='500c')

add_derived_field('Ttot/T500c',function=_normalized_total_temperature_profile,
                  combine_function=calculate_normalized_total_temperature_profile
                  , M_delta='M_total_500c',delta='500c')

# add_derived_field('R/R200m',function=_radial_normalization,
#                   combine_function=normalize_profile, r_delta_type='r200m'
#                   )

# add_derived_field('Tnt/T200m',function=_nomalized_total_temperature_profile,
#                   combine_function=calculate_normalized_nonthermal_temperature_profile,
#                   M_delta='M_total_200m',delta='200m')

# add_derived_field('Ttot/T200m',function=_normalized_total_temperature_profile,
#                   combine_function=calculate_normalized_total_temperature_profile,
#                   M_delta='M_total_200m',delta='200m')

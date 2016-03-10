from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.derived_fields.derived_field_tools.non_thermal_temperature \
    import calculate_T_nonthermal
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_T_normalization
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.plotting.profiles.tools.make_profile import make_profile


def _normalized_nonthermal_temperature_profile(data, *args, **kwargs) :

    Mvir = data.halo_properties[kwargs['M_delta_key']]
    sigr=data.profiles['vel_gas_rad_std']
    sigt=data.profiles['vel_gas_tan_std']
    vr = data.profiles['vel_gas_rad_avg']
    vt = data.profiles['vel_gas_tan_avg']

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({ 'sigr':sigr, 'sigt':sigt, 'vr':vr, 'vt':vt, 
                  'aexp':data.aexp, 'Mvir':Mvir, 'Rscaled':Rscaled,
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
        normalized_Tnt[hid] = make_profile(x=d['Rscaled'][hid],y=normalized_Tnt[hid])

    return normalized_Tnt


add_derived_field('Tnt/T500c',function=_normalized_nonthermal_temperature_profile,
                  combine_function=calculate_normalized_nonthermal_temperature_profile
                  , M_delta_key='M_total_500c', R_delta_key='r500c',
                  delta='500c')

add_derived_field('Tnt/T200m',function=_normalized_nonthermal_temperature_profile,
                  combine_function=calculate_normalized_nonthermal_temperature_profile,
                  M_delta_key='M_total_200m', R_delta_key='r200m',
                  delta='200m')

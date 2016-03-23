from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_S_normalization
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.circular_velocity.derived_field_functions \
    import calculate_vcirc2
from L500analysis.utils.constants import km2cm,km2m
from L500analysis.plotting.profiles.tools.make_profile import make_profile_linear

def _normalized_radial_velocity_profile(data, *args, **kwargs) :

    V_r = data.profiles['vel_gas_rad_avg']

    Mvir = data.halo_properties[kwargs['M_delta_key']]

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({ 'aexp':data.aexp, 'Mvir':Mvir, 'Rvir':Rvir, 
                  'V_r':V_r,
                  'halo_ids':data.halo_ids, 
                  'Rscaled':Rscaled }, 
                **kwargs)

def calculate_normalized_radial_velocity_profile(input_data) :

    d = input_data
    normalized_Vr = {}
    for hid in d['halo_ids'] :
        Vcirc = calculate_vcirc2(mass_Msun=d['Mvir'][hid], 
                                 radius_kpc=d['Rvir'][hid])

        normalized_Vr[hid] = 1.-d['V_r'][hid]*km2m/Vcirc
        normalized_Vr[hid] = make_profile_linear(x=d['Rscaled'][hid],y=normalized_Vr[hid])
    return normalized_Vr


add_derived_field('VrVc_ratio_500c',function=_normalized_radial_velocity_profile,
                 combine_function=calculate_normalized_radial_velocity_profile, 
                  M_delta_key='M_total_500c', R_delta_key='r500c',
                  delta='500c')

add_derived_field('VrVc_ratio_200m',function=_normalized_radial_velocity_profile,
                 combine_function=calculate_normalized_radial_velocity_profile, 
                  M_delta_key='M_total_200m', R_delta_key='r200m',
                  delta='200m')


from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.plotting.profiles.tools.make_profile import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.temperature.derived_field_functions \
    import *
from L500analysis.utils.constants import keV2erg, mu,mp,km2cm, kb

def _Tmw_cm_per_s_2(data, *args, **kwargs) :
    
    T_mw = data.profiles['T_mw']

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({'Rmid':Rmid, 
                 'Rvir':Rvir,
                 'Rscaled':Rscaled, 
                 'T_mw':T_mw,
                 'halo_ids':data.halo_ids},
                **kwargs)

def _Vr2_cm_per_s_2(data, *args, **kwargs) :
    V_r = data.profiles['vel_gas_rad_avg']

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({'Rmid':Rmid, 
                 'Rvir':Rvir,
                 'Rscaled':Rscaled, 
                 'V_r':V_r,
                 'halo_ids':data.halo_ids},
                **kwargs)

def calculate_Tmw_cm_per_s_2(input_data) :
    d = input_data
    Tmw_cm_per_s_2 = {}
    for hid in d['halo_ids'] :
        Tmw_erg = d['T_mw'][hid] * kb
        Tmw_cm_per_s_2[hid] = make_profile(x=d['Rscaled'][hid],
                                      y=Tmw_erg/mu/mp)

    return Tmw_cm_per_s_2

def calculate_Vr2_cm_per_s_2(input_data) :
    d = input_data
    Vr_cm_per_s_2 = {}
    for hid in d['halo_ids'] :
        Vr_cm_per_s_2[hid] = make_profile(x=d['Rscaled'][hid],
                                     y=(d['V_r'][hid] * km2cm)**2)

    return Vr_cm_per_s_2
    


add_derived_field('Tmw_cm_per_s_2_r200m',
                  function=_Tmw_cm_per_s_2,
                  combine_function=calculate_Tmw_cm_per_s_2,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

add_derived_field('Vr2_cm_per_s_2_r200m',
                  function=_Vr2_cm_per_s_2,
                  combine_function=calculate_Vr2_cm_per_s_2,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

add_derived_field('Tmw_cm_per_s_2_r500c',
                  function=_Tmw_cm_per_s_2,
                  combine_function=calculate_Tmw_cm_per_s_2,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')

add_derived_field('Vr2_cm_per_s_2_r500c',
                  function=_Vr2_cm_per_s_2,
                  combine_function=calculate_Vr2_cm_per_s_2,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')


# add_derived_field('Tmw_Vr2_ratio_500c',
#                   function=_Tmw_vr2_ratio,
#                   combine_function=calculate_Tmw_vr2_ratio,
#                   R_delta_key='r500c',
#                   M_delta_key='M_total_500c')

# add_derived_field('Tmw_Vr2_ratio_200m',
#                   function=_Tmw_vr2_ratio,
#                   combine_function=calculate_Tmw_vr2_ratio,
#                   R_delta_key='r200m',
#                   M_delta_key='M_total_200m')

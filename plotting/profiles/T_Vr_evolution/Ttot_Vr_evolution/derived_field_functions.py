from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.plotting.profiles.tools.make_profile import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.temperature.derived_field_functions \
    import *
from L500analysis.utils.constants import keV2erg, mu,mp,km2cm, kb

def _Ttot_cm_per_s_2(data, *args, **kwargs) :

    sigr=data.profiles['vel_gas_rad_std']
    sigt=data.profiles['vel_gas_tan_std']
    vr = data.profiles['vel_gas_rad_avg']
    vt = data.profiles['vel_gas_tan_avg']

    T_mw = data.profiles['T_mw']

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({'Rmid':Rmid, 
                 'Rvir':Rvir,
                 'Rscaled':Rscaled, 
                 'sigr':sigr, 'sigt':sigt,
                 'vr':vr, 'vt':vt,
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

def calculate_Ttot_cm_per_s_2(input_data) :
    d = input_data
    Ttot_cm_per_s_2 = {}
    for hid in d['halo_ids'] :
        Ttot_erg = keV2erg*calculate_Ttot(sigr=d['sigr'][hid],vr=d['vr'][hid],
                                         sigt=d['sigt'][hid],vt=d['vt'][hid],
                                          Tmw=d['T_mw'][hid])
        

        Ttot_cm_per_s_2[hid] = make_profile(x=d['Rscaled'][hid],
                                           y=Ttot_erg/mu/mp)

    return Ttot_cm_per_s_2

def calculate_Vr2_cm_per_s_2(input_data) :
    d = input_data
    Vr_cm_per_s_2 = {}
    for hid in d['halo_ids'] :
        Vr_cm_per_s_2[hid] = make_profile(x=d['Rscaled'][hid],
                                     y=(d['V_r'][hid] * km2cm)**2)

    return Vr_cm_per_s_2
    


add_derived_field('Ttot_cm_per_s_2_r200m',
                  function=_Ttot_cm_per_s_2,
                  combine_function=calculate_Ttot_cm_per_s_2,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

add_derived_field('Vr2_cm_per_s_2_r200m',
                  function=_Vr2_cm_per_s_2,
                  combine_function=calculate_Vr2_cm_per_s_2,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

add_derived_field('Ttot_cm_per_s_2_r500c',
                  function=_Ttot_cm_per_s_2,
                  combine_function=calculate_Ttot_cm_per_s_2,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')

add_derived_field('Vr2_cm_per_s_2_r500c',
                  function=_Vr2_cm_per_s_2,
                  combine_function=calculate_Vr2_cm_per_s_2,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')



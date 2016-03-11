from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.circular_velocity.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.temperature.derived_field_functions \
    import *
from L500analysis.utils.constants import keV2erg, mu,mp,km2cm, kb

def _Tmw_vcirc2_ratio(data, *args, **kwargs) :
    
    T_mw = data.profiles['T_mw']

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    Mtot={hid: data.profiles['M_dark'][hid] + \
              data.profiles['M_gas'][hid] + \
              data.profiles['M_star'][hid] \
              for hid in data.halo_ids}

    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({'M_tot':Mtot, 'Rmid':Rmid, 
                 'Rvir':Rvir,
                 'Rscaled':Rscaled, 
                 'T_mw':T_mw,
                 'halo_ids':data.halo_ids},
                **kwargs)


def calculate_Tmw_vcirc2_ratio(input_data) :
    d = input_data
    Tmw_Vcirc2_ratio = {}
    for hid in d['halo_ids'] :
        Tmw_in_erg = d['T_mw'][hid] * kb

        Vcirc2 = calculate_vcirc2(mass_Msun=d['M_tot'][hid],
                                  radius_kpc=d['Rmid'][hid])

        Tmw_Vcirc2_ratio[hid] = make_profile(x=d['Rscaled'][hid],
                                              y=Tmw_in_erg/Vcirc2/mu/mp/km2cm**2)

    return Tmw_Vcirc2_ratio

add_derived_field('Tmw_Vcirc2_ratio_500c',
                  function=_Tmw_vcirc2_ratio,
                  combine_function=calculate_Tmw_vcirc2_ratio,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')

add_derived_field('Tmw_Vcirc2_ratio_200m',
                  function=_Tmw_vcirc2_ratio,
                  combine_function=calculate_Tmw_vcirc2_ratio,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

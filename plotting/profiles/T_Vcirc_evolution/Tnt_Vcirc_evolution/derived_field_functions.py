from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.circular_velocity.derived_field_functions \
    import *
from L500analysis.derived_fields.collections.temperature.derived_field_functions \
    import *
from L500analysis.utils.constants import keV2erg, mu,mp,km2cm

def _Tnt_vcirc2_ratio(data, *args, **kwargs) :
    
    T_mw = data.profiles['T_mw']
    Mvir = data.halo_properties[kwargs['M_delta_key']]
    sigr=data.profiles['vel_gas_rad_std']
    sigt=data.profiles['vel_gas_tan_std']
    vr = data.profiles['vel_gas_rad_avg']
    vt = data.profiles['vel_gas_tan_avg']

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    Mtot={hid: data.profiles['M_dark'][hid] + \
              data.profiles['M_gas'][hid] + \
              data.profiles['M_star'][hid] \
              for hid in data.halo_ids}

    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({'M_tot':Mtot, 'Rmid':Rmid, 
                 'Mvir':Mvir, 'Rvir':Rvir,
                 'Mvir':Mvir, 'Rscaled':Rscaled, 
                 'sigr':sigr, 'sigt':sigt, 
                 'vr':vr, 'vt':vt,
                 'T_mw':T_mw,
                 'halo_ids':data.halo_ids},
                **kwargs)


def calculate_Tnt_vcirc2_ratio(input_data) :
    d = input_data
    Tnt_Vcirc2_ratio = {}
    for hid in d['halo_ids'] :

        Tnt = calculate_T_nonthermal(sigr=d['sigr'][hid],vr=d['vr'][hid],
                                      sigt=d['sigt'][hid],vt=d['vt'][hid])

        Vcirc2 = calculate_vcirc2(mass_Msun=d['M_tot'][hid],
                                  radius_kpc=d['Rmid'][hid])

        Tnt_Vcirc2_ratio[hid] = make_profile(x=d['Rscaled'][hid],
                                              y=Tnt*keV2erg/Vcirc2/mu/mp/km2cm**2)

    return Tnt_Vcirc2_ratio

add_derived_field('Tnt_Vcirc2_ratio_500c',
                  function=_Tnt_vcirc2_ratio,
                  combine_function=calculate_Tnt_vcirc2_ratio,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')

add_derived_field('Tnt_Vcirc2_ratio_200m',
                  function=_Tnt_vcirc2_ratio,
                  combine_function=calculate_Tnt_vcirc2_ratio,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

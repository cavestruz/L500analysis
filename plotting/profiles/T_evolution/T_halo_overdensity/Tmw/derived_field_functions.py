from L500analysis.derived_fields.derived_fields import add_derived_field
from L500analysis.derived_fields.derived_field_tools.integrated_halo_properties \
    import CalculateHaloProperties as CHP
from L500analysis.plotting.profiles.T_evolution.Tall_evolution.derived_field_functions \
    import *
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_T_normalization
from L500analysis.utils.constants import K2keV
from L500analysis.plotting.profiles.tools.make_profile import make_profile
from L500analysis.derived_fields.collections.radial_normalizations.derived_field_functions import *

def _normalized_temperature_profile(data, *args, **kwargs) :

    T_mw = data.profiles['T_mw']
    Mgas = data.profiles['M_gas']
    Mdark = data.profiles['M_dark']
    Mstar = data.profiles['M_star']

    Mtot = {hid: Mgas[hid]+Mdark[hid]+Mstar[hid] for hid in data.halo_ids}

    Rmid = data.profiles['r_mid']

    return dict({ 'aexp':data.aexp, 'Mtot':Mtot, 
                  'T_mw':T_mw,
                  'halo_ids':data.halo_ids, 
                  'Rmid':Rmid }, 
                **kwargs)

def calculate_normalized_temperature_profile(input_data) :

    d = input_data
    normalized_T = {}
    for hid in d['halo_ids'] :
        integrated_halo_props = CHP(physical_radial_profile=d['Rmid'][hid],
                                    mass_enclosed_profile=d['Mtot'][hid],
                                    delta=d['delta'],
                                    aexp=d['aexp'])

        Tdelta = calculate_T_normalization(Mvir=integrated_halo_props.calculate_virial_mass(),
                                          delta=d['delta'],
                                          aexp=d['aexp'])
        
        Rscaled = d['Rmid'][hid]/integrated_halo_props.calculate_virial_radius()
                                          
        normalized_T[hid] = d['T_mw'][hid]*d['units']/Tdelta

        normalized_T[hid] = make_profile(x=Rscaled,y=normalized_T[hid])

    return normalized_T


add_derived_field('T_mw/T1600c',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  delta='1600c',units=K2keV)

add_derived_field('T_mw/T500c',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  delta='500c',units=K2keV)

add_derived_field('T_mw/T200c',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  delta='200c',units=K2keV)

add_derived_field('T_mw/T1600m',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  delta='1600m',units=K2keV)

add_derived_field('T_mw/T500m',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  delta='500m',units=K2keV)

add_derived_field('T_mw/T200m',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  delta='200m',units=K2keV)



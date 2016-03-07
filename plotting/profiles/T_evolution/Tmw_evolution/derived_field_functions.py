from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_T_normalization
from L500analysis.plotting.profiles.tools.radial_normalizations import *

def _normalized_temperature_profile(data, *args, **kwargs) :

    T_mw = data.profiles['T_mw']
    Mvir = data.halo_properties[kwargs['M_delta_key']]

    return dict({ 'aexp':data.aexp, 'Mvir':Mvir, 'T_mw':T_mw,
                  'halo_ids':data.halo_ids }, **kwargs)

def calculate_normalized_temperature_profile(input_data) :

    d = input_data
    normalized_T = {}
    for hid in d['halo_ids'] :
        Tdelta = calculate_T_normalization(Mvir=d['Mvir'][hid],
                                          delta=d['delta'],
                                          aexp=d['aexp'])

        normalized_T[hid] = d['T_mw'][hid]/Tdelta

    return normalized_T


add_derived_field('T_mw/T500c',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  M_delta_key='M_total_500c', delta='500c',units='K2keV')

add_derived_field('T_mw/T200m',function=_normalized_temperature_profile,
                 combine_function=calculate_normalized_temperature_profile, 
                  M_delta_key='M_total_200m', delta='200m',units='K2keV')


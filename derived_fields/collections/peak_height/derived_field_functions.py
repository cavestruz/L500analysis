from L500analysis.plotting.profiles.T_evolution.Tmw_evolution.derived_field_functions \
    import *
from L500analysis.plotting.profiles.T_evolution.Tnt_evolution.derived_field_functions \
    import *
from L500analysis.plotting.profiles.T_evolution.Ttot_evolution.derived_field_functions \
    import *
from L500analysis.derived_fields.derived_field_tools.cosmology_dependent_properties \
    import calculate_peak_height


def _peak_height(data, *arg, **kwargs) :
    Mvir = data.halo_properties[kwargs['M_delta_key']]

    return dict({ 'aexp':data.aexp, 'Mvir':Mvir,
                  'halo_ids':data.halo_ids }, **kwargs)


def get_peak_height(input_data) :

    d = input_data
    peak_height = {}
    for hid in d['halo_ids'] :
        peak_height[hid] = calculate_peak_height(Mvir=d['Mvir'][hid],
                                                 aexp=d['aexp'])

    return peak_height

add_derived_field('nu_500c',function=_peak_height,
                 combine_function=get_peak_height,
                  M_delta_key='M_total_500c', delta='500c')

add_derived_field('nu_200m',function=_peak_height,
                 combine_function=get_peak_height,
                  M_delta_key='M_total_200m', delta='200m')

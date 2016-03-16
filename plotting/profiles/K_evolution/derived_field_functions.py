from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_S_normalization
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.utils.constants import K2keV
from L500analysis.plotting.profiles.tools.make_profile import make_profile

def _normalized_entropy_profile(data, *args, **kwargs) :

    S_mw = data.profiles['S_mw']
    Mvir = data.halo_properties[kwargs['M_delta_key']]

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({ 'aexp':data.aexp, 'Mvir':Mvir, 'S_mw':S_mw,
                  'halo_ids':data.halo_ids, 
                  'Rscaled':Rscaled }, 
                **kwargs)

def calculate_normalized_entropy_profile(input_data) :

    d = input_data
    normalized_S = {}
    for hid in d['halo_ids'] :
        Sdelta = calculate_S_normalization(Mvir=d['Mvir'][hid],
                                          delta=d['delta'],
                                          aexp=d['aexp'])
        
        normalized_S[hid] = d['S_mw'][hid]*d['units']/Sdelta

        normalized_S[hid] = make_profile(x=d['Rscaled'][hid],y=normalized_S[hid])

    return normalized_S


add_derived_field('S_mw/S500c',function=_normalized_entropy_profile,
                 combine_function=calculate_normalized_entropy_profile, 
                  M_delta_key='M_total_500c', R_delta_key='r500c',
                  delta='500c',units=1)

add_derived_field('S_mw/S200m',function=_normalized_entropy_profile,
                 combine_function=calculate_normalized_entropy_profile, 
                  M_delta_key='M_total_200m', R_delta_key='r200m',
                  delta='200m',units=1)


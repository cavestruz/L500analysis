from L500analysis.derived_fields.derived_fields import *
from numpy import *
import copy

def sum_profiles( input_profiles=None ) :

    summed_profile = copy.deepcopy(input_profiles[0])
    halo_ids = summed_profile.keys()

    for hid in halo_ids :
        for input_profile in input_profiles[1:] :
            summed_profile[hid] += input_profile[hid]
    return summed_profile

def normalize_profile(input_data) :
    
    normalized_profile = copy.deepcopy(input_data['profile'])
    halo_ids = normalized_profile.keys()

    for hid in halo_ids :
        normalized_profile[hid] /= input_data['normalization'][hid]
    return normalized_profile

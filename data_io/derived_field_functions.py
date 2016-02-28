


def _total_halo_mass(profiles, *args, **kwargs) :

    halo_id = kwargs['halo_id']
    
    return [ profiles['M_dark'], 
             profiles['M_dark'], 
             profiles['M_dark'] ]


def sum_profiles( input_profiles ) :
    summed_profile = input_profiles[0]

    for input_profile in input_profiles[1:] :
        summed_profile = summed_profile+input_profile

    return summed_profile

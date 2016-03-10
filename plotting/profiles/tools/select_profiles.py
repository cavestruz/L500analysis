def nu_cut(nu=None, threshold=None) :
    '''Halo ids of nu dictionary, satisfying a nu cut'''
    t_low = threshold[0]
    t_high = threshold[1]

    return [ hid for hid, nu_value in nu.items() \
                 if nu_value <= t_high and nu_value >= t_low ]


def prune_dict(d=None, k=None) :
    return {key:d[key] for key in k}

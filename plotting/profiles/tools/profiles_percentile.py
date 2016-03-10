import numpy as np

def calculate_profiles_percentile( profiles, percentile=50 ) :

    return np.percentile(np.array(profiles.values()),
                         percentile,
                         axis=0)

def calculate_profiles_mean_variance( profiles,mean=None ) :

    if mean == None : mean = np.mean(profiles.values(),axis=0)
    var = np.var(np.array(profiles.values()),axis=0)

    return {'mean':mean, 'var':var, 'up': mean-var, 'down':mean-var}

def calculate_profiles_division_mean_variance( profiles1, 
                                               profiles2 ) :

    p1mean = np.mean(profiles1) 
    p2mean = np.mean(profiles2) 
    mean = p1mean/p2mean
    
    var1 = calculate_profiles_mean_variance(profiles1,p1mean)['var']
    var2 = calculate_profiles_mean_variance(profiles2,p2mean)['var']
    var = p1mean*var2 + p2mean*var1

    return {'mean':mean, 'var':var, 'up':mean+var, 'down':mean-var}

def get_profiles_division_mean_variance( mean_profile1=None,
                                         mean_profile2=None,
                                         var_profile1=None,
                                         var_profile2=None ) :
    
    mean = mean_profile1 / mean_profile2
    var = mean_profile1*var_profile2 + mean_profile2*var_profile1

    return {'mean':mean, 'var':var, 'up':mean+var, 'down':mean-var}

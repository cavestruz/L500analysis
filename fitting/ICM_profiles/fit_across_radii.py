''' 
Uses collect_samples to collect samples at each radius for features
and targets.  Plots the predicted radial profile.
'''
import load_samples_dimensions as lsd
import numpy as np
import matplotlib.pyplot as plt
from L500analysis.utils.constants import rbins, linear_rbins
from test_load_samples import collect_samples, fit_samples
from collections import defaultdict
from itertools import product


def generate_models(data=None) :
    '''
    With the data, generates a model for each radial bin
    |    Parameters 
    |    -----------
    |      data : loaded_sample object
    |
    |    Returns 
    |    -------
    |      models : a list of linear_model.LinearRegression() 
    |              objects that have been fit to the data 
    '''

    models = []

    # Loop over each radius
    for radial_bin in range(len(rbins)) :
        
        samples = collect_samples(data=data,
                                  features_keys=['nu_500c'],
                                  targets_keys=['T_mw/T500c'],
                                  radial_bin=radial_bin,
                                  train_size=0.95)
        # Train the model on the training sample
        models.append(fit_samples(**samples)['trained_model'])

    return models

def generate_model_profiles(nu_vals=[1.5], aexps=[1.0], 
                            trained_models=None) :
    '''
    Loops through each radius and generates the model profile at each
    radial point.  Does this for each (nu, aexp) pair from the
    specified parameters.
    |    Parameters 
    |    ----------
    |    nu_vals : a list of peak heights
    |    aexps : a list of aexps
    |    trained_models : a list of trained models at each radial bin
    '''
    profiles = defaultdict(list)


    # Create nu, aexp pairs
    profile_keys = list(product(nu_vals,aexps))

    # Generate a profile for each (nu, aexp) pair
    for pk in profile_keys :
        for trained_model in trained_models :
            profiles[pk].append(trained_model.predict(pk))

    # Convert to a numpy array
    profiles = {pk: np.array(profiles[pk]) for pk in profile_keys}
    
    return profiles

def plot_model_profiles() :
    '''
    Plot the model results for all radii at given nu and aexp.
    '''
    pass

if __name__ == "__main__"  :

    loaded_sample = lsd.load_sample()

    models = generate_models(data=loaded_sample) 

    model_profiles = generate_model_profiles(
        trained_model=models)

    plot_model_profiles()

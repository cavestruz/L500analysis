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
from matplotlib import cm
colors = cm.afmhot_r

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
                                  features_keys=['nu_200m'],
                                  targets_keys=['T_mw/T200m'],
                                  radial_bin=radial_bin,
                                  train_size=.99)
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
            profiles[pk].append(trained_model.predict(pk)[0][0])

    # Convert each model profile from list to a numpy array
    profiles = {pk: np.array(profiles[pk]) for pk in profile_keys}

    return profiles

def plot_model_profiles(model_profiles=None,nu_vals=None) :
    '''
    Plot the model results for all radii at given nu and aexp.
    '''
    figs = dict(zip(nu_vals, [plt.figure(figsize=(7,7)) for nu_val in nu_vals]))
    profile_keys = sorted(model_profiles.keys(), key=lambda x: x[1])
    for profile_key in profile_keys :
        nu_val, aexp = profile_key
        ax = figs[nu_val].gca()
        ax.plot(rbins, model_profiles[profile_key], color=colors(aexp),label='z=%.2f'%(1./aexp-1.))

    for nu_val, fig in figs.iteritems() : 
        fig.gca().set_xlim((0.2,4.0))
        fig.gca().set_xlabel('R/R200m',fontsize='xx-large')
        fig.gca().set_ylim((0,1.2))
        fig.gca().set_ylabel('T/T200m',fontsize='xx-large')
        fig.gca().legend()
        fig.gca().annotate('$\\nu_{200m}$='+str(nu_val),(0.5,1.0),fontsize='xx-large')
        fig.savefig('fitting_figs/model_T_profile_nu_'+str(nu_val)+'_200m.pdf')

if __name__ == "__main__"  :

    aexps = np.arange(0.4,1.1,0.1)
    loaded_sample = lsd.load_sample(aexps=aexps)

    nu_vals = [1.6,1.8,2.0,2.2,2.4,2.6]

    models = generate_models(data=loaded_sample) 

    model_profiles = generate_model_profiles(
        nu_vals=nu_vals, aexps=aexps,
        trained_models=models)

    plot_model_profiles(model_profiles=model_profiles,nu_vals=nu_vals)

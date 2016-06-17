''' 
Test the linear regression functionality from scipy on the temperature
profiles, then also the density profiles (or just Yx)

Ultimate "mini" goal: Predict T/T200m at a given R/R200m (e.g. rbins)
as a function of nu and z.
''' 

import load_samples_dimensions as lsd
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from L500analysis.utils.constants import rbins, linear_rbins
from plot_parameters import plot_model_2d, plot_model_3d


def collect_samples(data=None, features_keys=None, targets_keys=None, 
                    radial_bin=len(rbins)*19/20,
                    test_split=True,train_size=0.9) :
    ''' 
    Need to get the cluster data into training and testing subsamples

     |      Parameters
     |      ----------
     |      data : cluster data with at least two features/targets that 
     |             will be put into numpy array or sparse matrix of shape 
     |             [n_samples,n_features] for Training data and
     |             [n_samples, n_targets] for Target values
     |            
     |      features_key : key of features (e.g. nu_200m, aexp, redshift)
     |      targets_key : key of targets (e.g. T/T200m)
     |      radial_bin : Radial bin to predict
     |      test_split : defaults to True to keep a subsample 
     |                   of data as a test_sample, using train_test_split method
     |      train_size : Fraction of data to keep as training.
    '''

    cld = data
    aexps = cld.keys()
    hids = {aexp: cld[aexp]['halo_ids'] for aexp in aexps}
    feature_samples = []
    target_samples = []
    for aexp in aexps :
        feature_samples += [[cld[aexp][key][hid] \
                                 for key in features_keys]+[aexp] 
                            for hid in hids[aexp]]
        target_samples += [[cld[aexp][key][hid][radial_bin] \
                                for key in targets_keys] \
                               for hid in hids[aexp] ]

    feature_samples = np.array(feature_samples)
    target_samples = np.array(target_samples)

    if test_split :
        train_test_samples = train_test_split(feature_samples,target_samples,
                                              train_size=train_size)
        return {'data_X_train':train_test_samples[0],
                'data_X_test':train_test_samples[1],
                'data_y_train':train_test_samples[2],
                'data_y_test':train_test_samples[3]
                }
        
    else :
        return {'data_X_train':feature_samples,
                'data_y_train':target_samples
                }

def fit_samples(**kw) :
    '''
    Step 1: For a single z and nu, get predicted T/T200m at given R/R200m value (e.g. rbins)
    Need a training X and y to run regression.fit, then can compare with the test.
    | fit_samples 
    |       Parameters:
    | data_X_train, data_y_train, 
    | data_X_test, data_y_test
    |

     |  fit(self, X, y, n_jobs=1)
     |      Fit linear model.
     |      
     |      Parameters
     |      ----------
     |      X : numpy array or sparse matrix of shape [n_samples,n_features]
     |          Training data
     |      
     |      y : numpy array of shape [n_samples, n_targets]
     |          Target values
     |
     |  Returns: LinearRegression object that has been trained on the 
     |           training set,
     |           statistics,
     |           the training and the test data.
    '''

    # Create the linear regression object
    regr = linear_model.LinearRegression()
    
    # Train the model using the training set
    regr.fit(kw['data_X_train'], kw['data_y_train'])

    # The coefficients                                                                   
    coefficients = regr.coef_
    # The mean square error                                                         
    residual_sum_of_sq = \
        np.mean((regr.predict(kw['data_X_test']) - kw['data_y_test']) ** 2)
    # Explained variance score: 1 is perfect prediction                                 
    variance_score = regr.score(kw['data_X_test'], kw['data_y_test'])

    return dict({'trained_model' : regr,
                 'coefficients' : coefficients,
                 'residual_sum_of_sq' : residual_sum_of_sq,
                 'variance_score' : variance_score},
                **kw
                )



if __name__ == "__main__"  :

    loaded_sample = lsd.load_sample()
    samples = collect_samples(data=loaded_sample, 
                              features_keys=['nu_500c'], 
                              targets_keys=['T_mw/T500c'],
                              test_split=True)
    model_results = fit_samples(**samples)
    
    plot_model_2d( data_X_test=model_results['data_X_test'], 
                   data_y_test=model_results['data_y_test'],
                   data_X_train=model_results['data_X_train'], 
                   data_y_train=model_results['data_y_train'],
                   trained_model=model_results['trained_model'],
                   xlabel='nu_500c',
                   ylabel='Tmw/T500c(R/R500c=3)',
                   figname='r500c_3',
                   )
    

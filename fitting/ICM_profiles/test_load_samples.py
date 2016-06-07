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

cldata = lsd.load_sample()

def collect_samples(data=None, features_keys=None, targets_keys=None, 
                    radial_bin=len(rbins)/2,
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

    cldata = data
    hids = cldata['halo_ids']
    feature_samples = np.array([ [cldata[key][hid] for key in features_keys] \
                                     for hid in hids])
    print 'targets_keys', targets_keys
    target_samples = np.array([[cldata[key][hid][radial_bin] \
                                    for key in targets_keys] \
                                    for hid in hids])

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

def fit_samples(data_X_train=None, data_y_train=None, 
                data_X_test=None, data_y_test=None) :
    '''
    Step 1: For a single z and nu, get predicted T/T200m at given R/R200m value (e.g. rbins)
    Need a training X and y to run regression.fit, then can compare with the test.
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

    '''

    # Create the linear regression object
    regr = linear_model.LinearRegression()
    
    # Train the model using the training set
    regr.fit(data_X_train, data_y_train)

    # The coefficients                                                                        
    print('Coefficients: \n', regr.coef_)
    # The mean square error                                                                   
    print("Residual sum of squares: %.2f"
          % np.mean((regr.predict(data_X_test) - data_y_test) ** 2))

    # Explained variance score: 1 is perfect prediction                                       
    print('Variance score: %.2f' % regr.score(data_X_test, data_y_test))


    # Plot outputs                                                                            
    plt.scatter(data_X_test, data_y_test,  color='black')
    plt.scatter(data_X_train, data_y_train, color='blue')
    plt.plot(data_X_test, regr.predict(data_X_test), color='blue',
             linewidth=2)

    plt.xticks(())
    plt.yticks(())

    plt.show()

if __name__ == "__main__"  :
    samples = collect_samples(data=cldata, features_keys=['nu_200m'], 
                              targets_keys=['T_mw/T200m'],
                              test_split=True)
    fit_samples(**samples)

### EDITING HERE: Got it working for ONE radius, need to do this for
### all AND need to do this for different redshifts/aexp (not sure
### which one yet...)

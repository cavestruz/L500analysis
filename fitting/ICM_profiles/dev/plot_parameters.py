'''
Plot two parameters in 3d projection
'''

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



def plot_model_2d(data_X_test=None, data_y_test=None,
                  data_X_train=None, data_y_train=None,
                  trained_model=None,figname='fig1',
                  xlabel='Feature', ylabel='Target') :
    '''
    Plots the features and targets for both the test and training set.
    Test set data points in black, training in blue.  Model's
    prediction is in the blue line.
    '''
    plt.scatter(data_X_test[:,0], data_y_test,  color='black', label='Test')
    plt.scatter(data_X_train[:,0], data_y_train, color='blue', label='Train',alpha=0.3)
    plt.plot(data_X_test[:,0], trained_model.predict(data_X_test), color='black',
             marker='*',markersize=14,label='Prediction',ls='None',alpha=0.6)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig('fitting_figs/'+figname+'.pdf')

def plot_model_3d(fig_num=None, elev=None, azim=None, X_train=None, 
              y_train=None, trained_model=None, X1label='X1', X2label='X2',
              Ylabel='Y'):
    '''
    Assigns a different figure for viewing the 3-d plot of two
    features values and the target values from different angles.

    |      Parameters                                                                    
    |      ----------                                                                    
    |      fig_num : Should be a unique integer compared with other figures.
    |                                                                                    
    |      elev : elevation/height of the 3d axis view (e.g. 43.5, -0.5)
    |      azim : azimuthal angle of viewing (e.g. -110, 0, 90)
    |      X_train : features from the training set to plot
    |      y_train : target numpy array from the training set to plot
    |      trained_model : linear_model.LinearRegression() object where the object has
    |            been trained and is ready to predict
    |      X1label : First feature name, a string
    |      X2label : Second feature name, a string
    |      Ylabel : Target name, a string
    '''

    fig = plt.figure(fig_num, figsize=(4, 3))
    plt.clf()

    ax = Axes3D(fig, elev=elev, azim=azim)

    ax.scatter(X_train[:, 0], X_train[:, 1], y_train, c='k', marker='+')
    ax.plot_surface(np.array([[-.1, -.1], [.15, .15]]),
                    np.array([[-.1, .15], [-.1, .15]]),
                    clf.predict(np.array([[-.1, -.1, .15, .15],
                                          [-.1, .15, -.1, .15]]).T
                                ).reshape((2, 2)),
                    alpha=.5)

    ax.set_xlabel(X1label)
    ax.set_ylabel(X2label)
    ax.set_zlabel(Ylabel)

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

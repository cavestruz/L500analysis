from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import numpy as np

class TrainModel :
    '''                                                                                                                                              
     |      Parameters                                                                                                                               
     |      ----------                                                                                                                               
     |      data_X : numpy array or sparse matrix of shape [n_samples,n_features]
     |                     ( Feature data )                                                                                                                              
     |      data_y : numpy array of shape [n_samples, n_targets]
     |                     ( Target values )
     |      
     |      train_size : Fraction of sample for training vs. testing.  Default is 0.9.
     |
     |      Attributes                                                                                                                               
     |      ----------                                                                                                                               
     |      trained_model :  Trained linear regression model that will output a target value on other values that are not necessarily in the training data 
     |      coefficients : Coefficients of the regression
     |      residual : Residual of the fit
     |      variance : Variance score on the regression
     |      train_test_samples : dictionary of the train/test split features and targets
     |                                                                                                                                         
     '''

    def __init__( self, features, targets, train_size=0.9 ) :
        '''This expects data_X, data_y, optional kw for train_size'''
        self.features = features
        self.targets = targets
        self.train_size = train_size

        self._test_split()

        self._train_model()

    def _test_split( self ) :
       ''' Saves a subset for tesing.'''
       assert( self.train_size > 0.0 and self.train_size < 1.0 )
       self.train_test_samples = dict(zip(['data_X_train', 'data_X_test',
                                           'data_y_train', 'data_y_test'],
                                          train_test_split(self.features, 
                                                           self.targets,
                                                           train_size=self.train_size)))
    def _train_model( self ) :
        # Create the linear regression object                                                                                                        
        regr = linear_model.LinearRegression()
    
        # Train the model using the training set                                                                                                     
        self.trained_model = regr.fit(self.train_test_samples['data_X_train'], 
                                      self.train_test_samples['data_y_train'])
        
        # The coefficients                                                                                                                           
        self.coefficients = regr.coef_


        # The mean square error                                                                                                                      
        self.residual_sum_of_sq = \
            np.mean((regr.predict(self.train_test_samples['data_X_test']) - \
                         self.train_test_samples['data_y_test']) ** 2)

        # Explained variance score: 1 is perfect prediction                                                                                          
        self.variance_score = regr.score(self.train_test_samples['data_X_test'], 
                                         self.train_test_samples['data_y_test'])

       

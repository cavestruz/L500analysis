from sklearn import linear_model
from sklearn.cross_validation import train_test_split

class TrainModel :
    '''                                                                                                                                              
     |      Parameters                                                                                                                               
     |      ----------                                                                                                                               
     |      data_X_train : numpy array or sparse matrix of shape [n_samples,n_features]
     |                     ( Training data )                                                                                                                              
     |      data_y_train : numpy array of shape [n_samples, n_targets]
     |                     ( Target values )
     |
     |      Attributes                                                                                                                               
     |      ----------                                                                                                                               
     |      trained_model :  Trained linear regression model that will output a target value on other values that are not necessarily in the training data 
     |      coefficients : Coefficients of the regression
     |      residual : Residual of the fit
     |      variance : Variance score on the regression
     |                                                                                                                                               
     '''

    def __init__( self, **kw ) :
        '''This expects data_X_train, data_y_train, data_X_test, data_y_test'''
        self._kw = kw


    def _test_split( self, train_size ) :
       ''' Run this if you want to save a subset for tesing.'''
       assert( train_size > 0.0 and train_size < 1.0 )
       train_test_samples = train_test_split(feature_samples,target_samples,
                                             train_size=train_size)
    def _train_model( self ) :
        # Create the linear regression object                                                                                                        
        regr = linear_model.LinearRegression()
    
        # Train the model using the training set                                                                                                     
        self.trained_model = regr.fit(self._kw['data_X_train'], self._kw['data_y_train'])
        
        # The coefficients                                                                                                                           
        self.coefficients = regr.coef_

        # The mean square error                                                                                                                      
        self.residual_sum_of_sq = \
            np.mean((regr.predict(self._kw['data_X_test']) - self._kw['data_y_test']) ** 2)

        # Explained variance score: 1 is perfect prediction                                                                                          
        self.variance_score = regr.score(self._kw['data_X_test'], self._kw['data_y_test'])

       

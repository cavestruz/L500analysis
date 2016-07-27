from sklearn import linear_model
from sklearn.cross_validation import train_test_split

class TrainModel :
    '''                                                                                                                                              
     |      Parameters                                                                                                                               
     |      ----------                                                                                                                               
     |      ??? :                                                                                                                      
     |                                                                                                                                               
     |      Attributes                                                                                                                               
     |      ----------                                                                                                                               
     |      ???? : 
     |                                                                                                                                               
     '''

    def __init__( self, **kw ) :
        pass


    def _test_split( self, train_size ) :
       ''' Run this if you want to save a subset for tesing.'''
       assert( train_size > 0.0 and train_size < 1.0 )
       train_test_samples = train_test_split(feature_samples,target_samples,
                                             train_size=train_size)
    def _train_model( self ) :
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

       

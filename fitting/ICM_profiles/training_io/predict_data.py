from itertools import product
from collections import defaultdict
import numpy as np

class PredictData :
    '''
    Take the features and trained models to make predicted targets

    |    Parameters
    |    ----------                                                                                                                                  
    |    features : lists containing the values of each feature
    |    trained_models : List of the trained models
    |    model_descriptions : optional kwarg, list of model descriptions
    |
    |
    |    Attributes
    |    ----------                                                                                                                                  
    |    predictions : A dictionary of predictions with features as keys
    |    model_descriptions : the input model descriptions, describes what has 
    |                         been predicted in the predictions value
    |
    '''

    def __init__( self, trained_models, *features, **kwargs ) :

        self.trained_models = trained_models
        self.features = self._generate_feature_combinations( *features ) 
        self.predictions = defaultdict(list)
        try : 
            self.model_descriptions = kwargs.pop('model_descriptions')
        except KeyError : 
            self.model_descriptions = None

        self._predict()

    def _generate_feature_combinations( self, *features ) :
        return [ feature_combo for feature_combo in product(*features) ]

    def _predict( self ) :
        for feature in self.features : 
            for trained_model in self.trained_models :
                self.predictions[feature].append(trained_model.predict(feature)[0][0])

        self.predictions = { feature : np.array(self.predictions[feature]) for feature in self.features }

    def plot( self, ) :
        ''' Automatically plot predicted data '''
        pass

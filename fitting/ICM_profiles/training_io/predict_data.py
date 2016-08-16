from itertools import product
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from L500analysis.utils.constants import rbins


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

    def plot( self, group_by=0, color_by=1, cmap_name='afmhot_r', legend=True, **kw) :
        ''' Automatically plot predicted data 
        |    Parameters
        |    ----------
        |    group_by : the index of the feature we wish to group co-plotted values by 
        |               (index in the predictions tuple)
        |    color_by : the index of the feature we wish to color by, and label in the legend
        |    Takes in regular plotting kwargs
        |    
        '''
        
        cmap = plt.get_cmap(cmap_name)

        # Create as many figures as unique group_by values
        figure_keys = set([feature[group_by] for feature in self.predictions.keys()])
        Norm_color = max([feature[color_by] for feature in self.predictions.keys()])

        figures = defaultdict(lambda: plt.figure())

        for features, predictions in self.predictions.iteritems() :
            figures[features[group_by]].gca().plot(rbins, predictions, 
                                                   color=cmap(features[color_by]/Norm_color), 
                                                   label=features[color_by], **kw)

        # if legend :
        #     for key in figures.keys() :
        #         handles, labels = figures[key].gca().get_legend_handles_labels()
        #         print handles
        #         print labels
        #         sorted_legend = [ (h, l) for (l, h) in sorted(zip( labels, handles )) ]
        #         figures[key].gca().legend(*sorted_legend)

        self.figures = figures
        

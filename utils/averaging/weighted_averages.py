''' '''
import numpy as np
from numpy import random, average
from L500analysis.utils.averages.probability_distributions import create_pdf
from L500analysis.utils.utils import match_nearest

class WeightedAverages :
    def __init__(self, probability_distribution='uniform random',
                 pdf_sample_size=1000, 
                 min_candidate=0, max_candidate=1) :
        '''Probability distribution defaults to a uniform random distribution. 
        In development: gaussian

        pdf_sample_size: The number of points evenly sampled from the pdf

        min_candidate: candidate value that corresponds to the first
        sample point in the pdf

        max_candidate: candidate value that corresponds to the first
        sample point in the pdf

        '''

        self.pdf_type = probability_distribution
        self.pdf_sample_size = pdf_sample_size
        self.min_candidate = min_candidate
        self.max_candidate = max_candidate

    def _create_pdf(self) :
        return create_pdf(self.pdf_sample_size, self.pdf_type)

    def _create_array_of_candidates(self) :

        separation = float(self.max_candidate-self.min_candidate)/self.pdf_sample_size
        candidates = np.array(self.min_candidate, self.max_candidate, separation)
        assert(len(candidates)==self.pdf_sample_size)
        return candidates

    def generate_random_set(self, number_of_items_in_set) :
        pdf = self._create_pdf()
        array_of_candidates = self._create_array_of_candidates()

        self._generated_set = random.choice( array_of_candidates, 
                                             number_items_in_set, 
                                             p=pdf )

    def match_sample_to_generated_set(self, sample=None) :
        return match_nearest(estimates=self._generated_set,
                             exactvals=sample)

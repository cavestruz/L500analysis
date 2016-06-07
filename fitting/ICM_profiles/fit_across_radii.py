''' 
Uses collect_samples to collect samples at each radius for features
and targets.  Plots the predicted radial profile.
'''
import load_samples_dimensions as lsd
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from L500analysis.utils.constants import rbins, linear_rbins

import L500analysis.fitting.ICM_profiles.training_io.parse_config as pc
import L500analysis.fitting.ICM_profiles.training_io.configure_model as cm
import L500analysis.fitting.ICM_profiles.training_io.training_set as ts
import L500analysis.fitting.ICM_profiles.training_io.training_steps as tst
import L500analysis.fitting.ICM_profiles.training_io.predict_data as pd


inifile = '/home/babyostrich/Documents/Repos/L500analysis/fitting/ICM_profiles/config_ini/temperature_test.ini'

# Load configuration parameters
MCP = pc.MyConfigParser(inifile) 

# Make output directories and output the configuration parameters for
# this model
cm.make_output(MCP.parsed_info)

# Load training samples, get the features and targets to run the model
CS = ts.CollectSamples(MCP.parsed_info)

#  Loop over radial bins for whole model
CS.set_radial_bin(30)
CS.get_targets()
CS.get_features()

# Train the model based on the data targets and features
model = tst.TrainModel(features=CS.features,targets=CS.targets)

# Predict targets based on desired features
X_aexps = [0.95, 0.75]
X_nu500c = [1.7, 2.5]
pd.PredictData( [model.trained_model],  X_aexps, X_nu500c ) 

# NEED TO MAKE A SEPARATE FUNCTION OR MODULE THAT GOES OVER RADII, and ALSO INTEGRATED QUANTITIES

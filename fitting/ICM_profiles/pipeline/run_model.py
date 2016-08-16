import L500analysis.fitting.ICM_profiles.training_io.parse_config as pc
import L500analysis.fitting.ICM_profiles.training_io.configure_model as cm
import L500analysis.fitting.ICM_profiles.training_io.training_set as ts
import L500analysis.fitting.ICM_profiles.training_io.training_steps as tst
import L500analysis.fitting.ICM_profiles.training_io.predict_data as pd
from L500analysis.utils.constants import rbins

inifile = '/home/babyostrich/Documents/Repos/L500analysis/fitting/ICM_profiles/config_ini/temperature_test.ini'

# Load configuration parameters
MCP = pc.MyConfigParser(inifile) 

# Make output directories and output the configuration parameters for
# this model
cm.make_output(MCP.parsed_info)

# Load training samples, get the features and targets to run the model
CS = ts.CollectSamples(MCP.parsed_info)

# Generate trained models
trained_models = [tst.get_trained_model(CS, ibin_radial=i).trained_model for i in range(len(rbins))]

# Predict targets based on desired features
X_aexps = [0.95, 0.75]
X_nu500c = [1.7, 2.5]

predicted_data = pd.PredictData( trained_models,  X_aexps, X_nu500c ) 

# Plot predicted data
predicted_data.plot(group_by=1, color_by=0, lw=2.0)

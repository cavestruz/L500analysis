import training_io.parse_config as pc
import training_io.configure_model as cm
import training_io.training_set as ts

inifile = '/home/babyostrich/Documents/Repos/L500analysis/fitting/ICM_profiles/config_ini/test_temperature.ini'


MCP = pc.MyConfigParser(inifile) 
cm.make_output(MCP.parsed_info)
CS = ts.CollectSamples(MCP.parsed_info)

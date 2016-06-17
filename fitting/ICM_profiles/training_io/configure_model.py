'''
Uses parsed data from the config file to create a model output
directory to initialize the model building.  Write to a .cfg file in
that directory with all of the initialization info.
'''

import os, ConfigParser

def make_output( parsed_info ) :
    '''Creates the directory for the output model, prints the config info to that as well'''
    for k, directory in parsed_info['OutputInfo'].iteritems() :
        if os.path.exists(directory) : 
            print('%s exists',directory)
        else :
            print('making %s',directory)
            os.makedirs(directory)
    inidir = parsed_info['OutputInfo']['modeldir']
    _write_config(parsed_info, inidir)

def _write_config(parsed_info, inidir) :
    config = ConfigParser.RawConfigParser()
    
    for section in parsed_info.keys() :
        config.add_section(section) 
        for options in parsed_info[section].keys() :
            config.set(section, options, parsed_info[section][options])
    
    with open(inidir+'/init.cfg', 'wb') as configfile :
        config.write(configfile)


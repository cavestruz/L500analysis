''' 
Load and parse the ini file to determine how and what models to build.

'''

import ConfigParser, json
from collections import defaultdict

class MyConfigParser :
    def __init__(self, inifile) :
        '''Returns a dictionary of config parameters'''
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(inifile)
        self.parsed_info = defaultdict(dict)
        self.get_asis_info()
        self.get_list_info()
        
    def _populate_json_list(self, section, option) :
        self.parsed_info[section][option] = \
            json.loads( self.cp.get(section, option) )

    def _populate_asis( self, section, option ) :
        self.parsed_info[section][option] = self.cp.get(section,option)

    def _populate_list( self, section, option ) :
        self.parsed_info[section][option] = \
            self.cp.get( section,option ).strip('[]').replace('\n','').replace(' ','').replace('\'','').split(',')

    def get_asis_info( self ) :
        for section in ['DataBaseInfo', 'OutputInfo'] :
            for option in self.cp.options(section) :
                self._populate_asis( section, option ) 

    def get_list_info( self ) :
        for section in ['LoadedTrainingData','TrainingInfo','ModelInfo'] :
            for option in self.cp.options(section) :
                self._populate_list( section, option ) 

    def get_json_list_info( self ) :
        pass
        for section in ['LoadedTrainingData','TrainingInfo','ModelInfo'] :
            for option in self.cp.options(section) :
                self._populate_json_list( section, option )
    


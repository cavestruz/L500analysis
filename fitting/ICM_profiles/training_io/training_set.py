'''
Use parsed config file to load training data
'''

from L500analysis.data_io.get_cluster_data import GetClusterData
# Note: will want the derived_field locations to be generally
# accessible - maybe in the config file, specify all the imports for
# derived fields?
from L500analysis.plotting.profiles.T_evolution.Tmw_evolution.derived_field_functions\
    import *
import numpy as np

def load_sample(parsed_info) :
    cld = {}
    for aexp in parsed_info['LoadedTrainingData']['aexps'] :
        GCD = GetClusterData(aexp=aexp,db_name=parsed_info['DataBaseInfo']['db_name'],
                             db_dir=parsed_info['DataBaseInfo']['db_dir'],
                             profiles_list=parsed_info['LoadedTrainingData']['profiles_list'],
                             halo_properties_list=parsed_info['LoadedTrainingData']['halo_properties_list'] 
                             )
        cld[GCD['aexp']] = GCD
    return cld


class CollectSamples :
    '''
     |      Parameters
     |      ----------
     |      parsed_info : the parsed_info dictionary from the parse_config.MyConfigParser 
     |                    object
     |
     |      Attributes
     |      ----------
     |      data : cluster data with at least two features/targets that 
     |             will be put into numpy array or sparse matrix of shape 
     |             [n_samples,n_features] for Training data and
     |             [n_samples, n_targets] for Target values
     |            
     |      features_key : key of features (e.g. nu_200m, aexp, redshift)
     |      targets_key : key of targets (e.g. T/T200m)
     |      radial_bin : Radial bin of profiles to train the model
     |      features : list of lists with shape [n_samples, n_features] for Training
     |      targets : list of lists with shape [n_samples, n_targets] for Training
     '''    

    def __init__( self, parsed_info ) :
        features_keys = parsed_info['TrainingInfo']['features_keys']
        targets_keys = parsed_info['TrainingInfo']['targets_keys']
        self.keys = {'Features': features_keys, 'Targets': targets_keys}
        self.sample = {}
        self.data = load_sample(parsed_info)
        self.radial_bin = None
        self._collect_hids()

    def _collect_hids( self ) :
        aexps = self.data.keys()
        self._hids = {aexp: self.data[aexp]['halo_ids'] for aexp in aexps}

    def _check_if_profile( self, aexp, key ) :
        try : 
            _hid = self.data[aexp][key].keys()[0]
            prop = self.data[aexp][key][_hid]
        except AttributeError :
            return False

        try : return (len(prop) > 1)
        except TypeError : return False

    def _check_radial_bin( self ) :
        try : 
            assert( self.radial_bin != None ) 
        except AssertionError :
            print("Oops, need to set the radial bin... i.e. self.set_radial_bin(30) ")
        
    def set_radial_bin( self, radial_bin ) :
        '''Radial bin must be an integer in the range of the length of any profile'''
        self.radial_bin = radial_bin

    def _init_sample( self, sample_type ) :
        self.sample[sample_type] = []
        
    def features( self ) :
        try : return np.array(self.sample['Features'])
        except ValueError : print('Did you run self.get_features()?')

    def targets( self ) :
        try : return np.array(self.sample['Targets'])
        except ValueError : print('Did you run self.get_targets()?')


    def get_features( self ) :
        self._init_sample('Features')
        for aexp in self.data.keys() :
            self.sample['Features'] += self._populate_sample(aexp, sample='Features')

    def get_targets( self ) :
        self._init_sample('Targets')
        for aexp in self.data.keys() :
            self.sample['Targets'] += self._populate_sample(aexp, sample='Targets')

    def _populate_sample( self, aexp, sample='Features' ) :
        samples = []
        for key in self.keys[sample] :
            if self._check_if_profile(aexp,key) :
                print sample,':',key,' is a radial prop'
                self._collect_radial_prop(aexp, key, samples) 
            else :
                print sample,':',key,' is a halo prop'
                self._collect_halo_prop(aexp, key, samples) 
        return samples

    def _collect_halo_prop( self, aexp, key, samples ) :
        for hid in self._hids[aexp] :
            try : samples.append( self.data[aexp][key][hid] )
            except IndexError : samples.append( self.data[aexp][key] )                 

    def _collect_radial_prop( self, aexp, key, samples ) :
        self._check_radial_bin()

        try :
            for hid in self._hids[aexp] :
                samples.append( self.data[aexp][key][hid][self.radial_bin] )
        except IndexError :
            print('Try setting different radial bin with self.set_radial_bin(radial_bin)') 
            

        


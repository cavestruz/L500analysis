from load_db import *
from get_derived_fields import *

class GetClusterData :
    def __init__(self,  aexp=None, db_name=None, db_dir=None,
                 profiles_list=[],
                 halo_properties_list=[]) :
        '''                                             
        kwargs 
        ------- 
        aexp: Expansion factor, does not need to be exact
        db_name: e.g. "L500_NR_0"
        db_dir: best to specify absolute path of database 
        profiles_list: available and derived profile fields to access
        halo_properties: available and derived halo properties to access
        '''

        self.ldb = LoadDataBase(aexp=aexp,db_name=db_name,db_dir=db_dir,
                              profiles_list=profiles_list, 
                              halo_properties_list=halo_properties_list)

        # Now all available profiles and halo properties are available
        # at this aexp are saved in dictionaries
        
        self.df = GetDerivedFields(loaded_data_object=self.ldb,
                                   profiles_list=profiles_list,
                                   halo_properties_list=halo_properties_list)


        # Now all derived profiles and halo properties are available
        # at this aexp and added to the dictionary


    def __getitem__(self, field=None) :

        if field in self.ldb.available_profiles_list :
            return self.ldb.profiles[field]
        elif field in self.ldb.derived_profiles_list :
            return self.df.profiles[field]
        
        elif field in self.ldb.available_halo_properties_list :
            return self.ldb.halo_properties[field]
        elif field in self.ldb.derived_halo_properties_list :
            return self.df.derived_halo_properties[field]
        elif field=='halo_ids' :
            return self.ldb.halo_ids
        else :
            raise KeyError('%s not a valid field' % name)

    def keys(self) :
        return self.available_profiles_list+self.derived_profiles_list+\
            self.available_halo_properties_list+self.derived_halo_properties_list+\
            ['halo_ids']
    

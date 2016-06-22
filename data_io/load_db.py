'''Load database, match to aexps needed'''
import sys
import numpy as np
import L500analysis.caps.io.reader as db
import L500analysis.utils.utils as ut

class LoadDataBase :
    def __init__(self, aexp=None, db_name="L500_NR_0", db_dir='../simulation_databases/',
                 profiles_list=None, 
                 halo_properties_list=None) :
        '''
        |        Parameters
        |        -------
        |        aexp: optional kwarg, list of aexps, does not need to be exact
        |        db_name: e.g. "L500_NR_0"
        |        db_dir: best to specify absolute path of database
        |        profiles_list: available and derived profile fields
        |        halo_properties_list: available and derived halo properties fields
        '''

        print("Loading database, executing queries... ")

        self.sim = db.Simulation(db_name,db_dir=db_dir)
        self._sort_profiles_list( profiles_list ) 
        self._sort_halo_properties_list( halo_properties_list ) 
        
        aexps = self.sim.get_halo_epochs()

        self.aexp = ut.match_nearest( [aexp], aexps )[0]

        self.halo_ids = self.sim.get_halo_ids(self.aexp) 
        self.halo_properties = self._get_halo_properties()
        self.profiles = self._get_profiles()

        self.sim.close()

    def _sort_profiles_list(self, profiles_list) :

        avail_profiles = self.sim.get_avail_properties(table='profiles')

        self.derived_profiles_list = [ profile for profile in profiles_list 
                                 if profile not in avail_profiles ]
        
        
        self.available_profiles_list = [ profile for profile in profiles_list 
                              if profile not in self.derived_profiles_list ]

    def _sort_halo_properties_list(self, halo_properties_list) :

        avail_properties = self.sim.get_avail_properties(table='halos')

        self.derived_halo_properties_list = [ hp for hp in halo_properties_list
                                         if hp not in avail_properties ]
        self.available_halo_properties_list = [ hp for hp in halo_properties_list
                                           if hp not in self.derived_halo_properties_list ]

    def _check_derived_profile_dependencies(self) :
        ''' Not implemented yet - will want this to check that all
        derived profile dependencies are added to available halo
        properties list before the database query'''
        for df in self.derived_profiles_list :
            pass
        

    def _check_derived_halo_dependencies(self) :
        ''' Not implemented yet - will want this to check that all
        derived halo properties dependencies are added to available
        halo properties list before the database query'''

        for dh in self.derived_halo_properties_list :
            pass
        
    
    def _get_halo_properties(self) :        
        if self.available_halo_properties_list != [] :
            return self.sim.get_halo_properties( 
                self.halo_ids, 
                self.available_halo_properties_list, 
                self.aexp, df=False )
        else :
            return None
        

    def _get_profiles(self) :
        if self.available_profiles_list != [] :
            return self.sim.get_halo_profiles( 
                self.halo_ids, 
                self.available_profiles_list, 
                self.aexp, df=False )
        else :
            return None


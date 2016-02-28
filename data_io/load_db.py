'''Load database, match to aexps needed'''
import sys
sys.path.append('../')
import numpy as np
import caps.io.reader as db
import utils as ut
from collections import defaultdict, OrderedDict


class LoadDataBase :
    def __init__(self, aexps=None, db_name="L500_NR_0", db_dir=None, 
                 profile_list=None, 
                 halo_properties_list=None) :
        '''
        kwargs
        -------
        aexp: optional kwarg, list of aexps, does not need to be exact
        db_name: e.g. "L500_NR_0"
        db_dir: best to specify absolute path of database
        profile_list: available and derived profile fields
        halo_properties_list: available and derived halo properties fields
        '''

        print("Loading database, executing queries... ")

        self.sim = db.Simulation(db_name,db_dir=db_dir)
        self._sort_profiles_list( profiles_list ) 
        self._sort_halo_properties( halo_properties_list ) 

        aexps = self.sim.get_halo_epochs()

        self.aexp = ut.match_nearest( [aexp], aexps )[0]

        self.halo_ids = self.sim.get_halo_ids(aexp) 
        self.halo_properties = self._get_halo_properties()
        self.profiles = self._get_profiles()


    def _sort_profiles_list(self, profile_list) :

        avail_profiles = self.sim.get_avail_properties(tables='profiles')

        self.derived_profiles_list = [ profile for profile in profile_list 
                                 if profile not in avail_profiles ]
        
        
        self.available_profiles_list = [ profile for profile in profile_list 
                              if profile not in self.derived_profiles ]

    def _sort_derived_halo_properties(self, halo_properties_list) :

        avail_properties = self.sim.get_avail_properties(tables='halos')

        self.derived_halo_properties_list = [ hp for hp in halo_properties_list
                                         if hp not in avail_properties ]
        self.available_halo_properties_list = [ hp for hp in halo_properties_list
                                           if hp not in self.derived_halo_properties ]

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


    def _derived_field( self, field=None, inputobject=None, **kwargs ) :
        '''Calls the derived field class for derived fields of already
        loaded data.'''

        dfc = DerivedFieldCollection( inputobject, **kwargs )
        return dfc.__getitem__(field)

    def add_items( self, ditems = None, aexps=None ) :
        '''Adds items that require some combination of profiles
        derived items.  Note, values that ditems depend on will need
        to have already been added.'''

        if type(ditems) != list :
            raise TypeError('ditems kwarg must be of type list')

        for aexp in self.aexps :
            hids = self._profile_data[aexp].keys()

            dval={ ditem:[ self._derived_field(name=ditem,
                                               inputobject=self._profile_data[aexp][hid])
                           for hid in hids ] for ditem in ditems }

            self._update_profile_data(aexp=aexp,items=dval, ids=hids)

        return



    def test_profiles(self, aexp) :
        
        profiles = self._get_profiles(aexp)
        for hid in self.sim.get_halo_ids(aexp)[:2] :
            print np.sum(profiles['M_dark'][hid], profiles['M_star'][hid], axis=1)


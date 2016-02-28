''' Create derived profiles from the database stored profiles '''

from derived_field_functions import *
from derived_fields import *

class GetDerivedFields :
    def __init__(self, loaded_data_object=None, 
                 profiles_list=None, 
                 halo_properties_list=None) :

        self.ldb = loaded_data_object

        self.profiles_list = [p for p in profiles_list \
                                  if p not in self.ldb.available_profiles_list]

        self.halo_properties_list = [hp for hp in halo_properties_list \
                                         if hp not in self.ldb.available_halo_properties_list]

        self.profiles = {}
        self.halo_properties = {}

        self._calculate_all_derived_fields()
        # Now all derived profiles and halo properties are stored

    def _calculate_all_derived_fields(self) :

        for field in self._ordered_fields_to_calculate() :
            self._store_field(field=field,
                              calculated_field=self._calculate_derived_field(field))

    def _ordered_fields_to_calculate(self) :
        '''Functionality not implemented yet.  Will want this to check
        for any dependencies in derived fields, and order them
        accordingly.'''

        return self.profiles_list+self.halo_properties_list

    def _store_field(self, field=None, calculated_field=None) :
        if field in self.profiles_list :
            self.profiles[field]=calculated_field
        elif field in self.halo_properties_list :
            self.halo_properties[field]=calculated_field

    def _calculate_derived_field(self,field) :
        dfc = DerivedFieldCollection(self.ldb) 
        return dfc.__getitem__(field)


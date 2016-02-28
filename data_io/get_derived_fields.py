''' Create derived profiles from the database stored profiles '''

from derived_field_functions import *

class GetDerivedFields :
    def __init__(self, loaded_data_object=None, 
                 profiles_list=None, 
                 halo_properties_list=None) :

        self.ldb = loaded_data_object

        self.profiles_list = [p for p in profiles_list \
                                  if not in self.ldb.available_profiles_list]

        self.halo_properties_list = [hp for p in halo_properties_list \
                                         if not in self.ldb.available_halo_properties_list]

        self.profiles = {}
        self.halo_properties = {}

        self.calculate_all_derived_fields()
        # Now all derived profiles and halo properties are stored

    def _calculate_all_derived_fields(self) :

        for field in self._ordered_fields_to_calculate() :
            self._store_field(field=field,
                              calculated_field=self.calculate_derived_field(field))

    def _ordered_fields_to_calculate(self) :
        '''Functionality not implemented yet.  Will want this to check
        for any dependencies in derived fields, and order them
        accordingly.'''

        return self.profiles_list+self.halo_properties_list

    def _store_field(self, field=None, calculated_field=None) :
        if field in self.profile_list :
            self.profile_list[field]=calculated_field
        elif field in self.halo_properties_list :
            self.halo_properties_list[field]=calculated_field

    def _calculate_derived_field(self,field) :
        dfc = DerivedFieldCollection(self) 
        return dfc.__getitem__(field)

class DerivedField :
    def __init__(self, dataobject=None, name=None, function=None,
                 combine_function=None, 
                 units=None, **kwargs) :

        self.__doc__ = function.__doc__
        self.__name__ = name
        self._inputobject = inputobject
        self.func = function
        self.c_func = combine_function
        self.kwargs = kwargs

    def __call__( self, *args, **kwargs ) :

        return self._call_function( args, **kwargs )

    def _call_function( self, *args, **kwargs ) :

        retval = self.func( self._inputobject, *args, **kwargs )
        return self.c_func( retval )


class DerivedFieldCollection :

    def __init__( self, inputobject) :
        self.inputobject = inputobject
        self.fields = derived_field_data

    def __getitem__( self, field ) :
        if field not in self.fields :
            raise KeyError('Need to construct functions for %s' % field )


        args = self.functions[field][:3]

        kwargs = self.functions[field][3]

        df = DerivedField(self.inputobject, *args, **kwargs)
        return df.__call__(self,*args,**kwargs)


    def keys( self ) :
        return self.functions.keys()



def add_derived_field( name, **kwargs ) :
    """ Takes keyword arguments function, and combine_function 

    Usage: add_derived_field( name, function=_field_function,
    combine_function=_combFunction )
    """

    if 'function' not in kwargs or 'combine_function' not in kwargs :
        raise Exception('function and combine_function required to derive %s' % name)
        return
    f = kwargs.pop("function")
    c = kwargs.pop("combine_function")
    derived_field_data[name] = (name, f, c, kwargs)

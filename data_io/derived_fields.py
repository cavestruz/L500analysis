'''

This module contains tools to derive fields other than those
directly pulled in with standard io.  Note that the
add_derived_function requires two keyword arguments (function and
combine_function), and these should likely be defined a module of
derived_field_functions that are applicable to a particular data set.

'''

derived_field_data = {}


class DerivedField :
    '''This is general 'call' function that makes the class
    callable. It simply redirets to _call_function right now, but this
    gives us flexibility to later add elif/switch statements to call
    different functions depending on what is needed
    '''

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
        print('Existing functions for ' % self.functions.keys())
        return self.functions.keys()


def add_derived_field( name, **kwargs ) :
    '''

    Takes keyword arguments function, and combine_function 

    Usage:
    add_derived_field( name, function=_field_function,
    combine_function=_combFunction )

    '''

    if 'function' not in kwargs or 'combine_function' not in kwargs :
        raise Exception('function and combine_function required to derive %s' % name)
        return
    f = kwargs.pop("function")
    c = kwargs.pop("combine_function")
    derived_field_data[name] = (name, f, c, kwargs)

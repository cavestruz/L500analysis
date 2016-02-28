'''Adds profile fields derived from profile fields in database'''

class AddFields(AddHaloProperties) :
    def __init__(self, derived_profiles=None, halo_properties=None) :

        AddHaloProperties.__init__(self, halo_properties=halo_properties)

        self.derived_fields = derived_profiles

    

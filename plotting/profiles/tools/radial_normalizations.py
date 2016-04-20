from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.derived_fields.derived_field_tools.integrated_halo_properties \
    import CalculateHaloProperties as CHP

def _radial_normalization(data,*args,**kwargs) :

    r_delta = kwargs['delta']

    return {'profile':data.profiles['r_mid'],
            'normalization':data.halo_properties[r_delta]}


add_derived_field('R/R500c',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r500c'
                  )


add_derived_field('R/R200m',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r200m'
                  )

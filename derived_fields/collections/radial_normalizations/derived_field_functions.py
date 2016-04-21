from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.derived_fields.derived_field_tools.integrated_halo_properties \
    import CalculateHaloProperties as CHP

def _get_radial_normalization( data, *args, **kwargs ) :
    
    Mgas = data.halo_properties[kwargs['M_gas']]
    Mdark = data.halo_properties[kwargs['M_dark']]
    Mstar = data.halo_properties[kwargs['M_star']]

    Mtot = {hid: Mgas[hid]+Mdark[hid]+Mstar[hid] for hid in data.halo_ids}


    r_delta = {hid: CHP(physical_radial_profile=data.profiles['r_mid'],
                        mass_enclosed_profile=Mtot[hid],
                        delta=kwargs['delta'],
                        aexp=data.aexp).calculate_virial_radius()\
                   for hid in data.halo_ids}
    
    return {'profile':data.profiles['r_mid'],
            'normalization':r_delta}

add_derived_field('R/R200c',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r200c'
                  )

add_derived_field('R/R500c',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r500c'
                  )

add_derived_field('R/R1600c',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r1600c'
                  )

add_derived_field('R/R200m',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r200m'
                  )

add_derived_field('R/R500m',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r500m'
                  )

add_derived_field('R/R1600m',function=_radial_normalization,
                  combine_function=normalize_profile, r_delta='r1600m'
                  )


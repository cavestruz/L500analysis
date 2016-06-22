from L500analysis.derived_fields.derived_fields import add_derived_field
from L500analysis.derived_fields.derived_field_functions import normalize_profile
from L500analysis.derived_fields.derived_field_tools.integrated_halo_properties \
    import CalculateHaloProperties as CHP

def _get_radial_normalization( data, *args, **kwargs ) :
    
    Mgas = data.profiles['M_gas']
    Mdark = data.profiles['M_dark']
    Mstar = data.profiles['M_star']

    Mtot = {hid: Mgas[hid]+Mdark[hid]+Mstar[hid] for hid in data.halo_ids}


    r_delta = {hid: CHP(physical_radial_profile=data.profiles['r_mid'][hid],
                        mass_enclosed_profile=Mtot[hid],
                        delta=kwargs['delta'],
                        aexp=data.aexp).calculate_virial_radius()\
                   for hid in data.halo_ids}
    
    return {'profile':data.profiles['r_mid'],
            'normalization':r_delta}

add_derived_field('R/R200c',function=_get_radial_normalization,
                  combine_function=normalize_profile, delta='200c'
                  )

add_derived_field('R/R500c',function=_get_radial_normalization,
                  combine_function=normalize_profile, delta='500c'
                  )

add_derived_field('R/R1600c',function=_get_radial_normalization,
                  combine_function=normalize_profile, delta='1600c'
                  )

add_derived_field('R/R200m',function=_get_radial_normalization,
                  combine_function=normalize_profile, delta='200m'
                  )

add_derived_field('R/R500m',function=_get_radial_normalization,
                  combine_function=normalize_profile, delta='500m'
                  )

add_derived_field('R/R1600m',function=_get_radial_normalization,
                  combine_function=normalize_profile, delta='1600m'
                  )


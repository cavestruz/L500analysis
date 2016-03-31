from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_tools.self_similar_normalizations \
    import calculate_rho_normalization
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.utils.constants import hubble,Msun2g,kpc2cm
from L500analysis.plotting.profiles.tools.make_profile import make_profile, calculate_dv

def _normalized_density_profile(data, *args, **kwargs) :

    M_gas = data.profiles[kwargs['gas_mass_key']]

    Rmid = data.profiles['r_mid']
    Rin = data.profiles['r_in']
    Rout = data.profiles['r_out']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({ 'aexp':data.aexp, 'M_gas':M_gas, 'Rmid':Rmid,
                  'Rin':Rin, 'Rout':Rout,
                  'halo_ids':data.halo_ids, 
                  'Rscaled':Rscaled }, 
                **kwargs)

def calculate_normalized_density_profile(input_data) :

    d = input_data
    normalized_rho = {}
    rho_delta = calculate_rho_normalization(delta=d['delta'],
                                            aexp=d['aexp'])
    for hid in d['halo_ids'] :
        dv = calculate_dv(rin=d['Rin'][hid],rout=d['Rout'][hid])
        rho = d['M_gas'][hid]/dv #Msun/kpc^3       
        normalized_rho[hid] = rho*d['units']/rho_delta
        normalized_rho[hid] = make_profile(x=d['Rscaled'][hid],y=normalized_rho[hid])

    return normalized_rho


add_derived_field('rhog_all/rho500c',function=_normalized_density_profile,
                  combine_function=calculate_normalized_density_profile, 
                  R_delta_key='r500c',gas_mass_key='M_gas_bin',
                  delta='500c',units=(hubble**2*Msun2g)/(kpc2cm)**3)

add_derived_field('rhog_all/rho200m',function=_normalized_density_profile,
                  combine_function=calculate_normalized_density_profile, 
                  R_delta_key='r200m',gas_mass_key='M_gas_bin',
                  delta='200m',units=(hubble**2*Msun2g)/(kpc2cm)**3)

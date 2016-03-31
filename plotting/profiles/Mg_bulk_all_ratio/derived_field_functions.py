from L500analysis.derived_fields.derived_fields import *
from L500analysis.plotting.profiles.tools.radial_normalizations import *
from L500analysis.derived_fields.collections.peak_height.derived_field_functions \
    import *
from L500analysis.utils.constants import hubble,Msun2g,kpc2cm
from L500analysis.plotting.profiles.tools.make_profile import make_profile

def _bulk_all_ratio_profile(data, *args, **kwargs) :

    M_gas_all = data.profiles['M_gas_bin']
    M_gas_bulk = data.profiles['M_gas_bulk_bin']
    Rmid = data.profiles['r_mid']
    Rin = data.profiles['r_in']
    Rout = data.profiles['r_out']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({ 'aexp':data.aexp, 'M_gas_bulk':M_gas_bulk,  'M_gas_all':M_gas_all,
                  'Rmid':Rmid,
                  'Rin':Rin, 'Rout':Rout,
                  'halo_ids':data.halo_ids, 
                  'Rscaled':Rscaled }, 
                **kwargs)

def calculate_bulk_all_ratio_profile(input_data) :

    d = input_data
    mass_ratio = {}
    
    for hid in d['halo_ids'] :
        mass_ratio[hid] = d['M_gas_bulk'][hid]/d['M_gas_all'][hid]
        mass_ratio[hid] = make_profile(x=d['Rscaled'][hid],y=mass_ratio[hid])

    return mass_ratio


add_derived_field('Mg_bulk/Mg_all_500c',function=_bulk_all_ratio_profile,
                  combine_function=calculate_bulk_all_ratio_profile, 
                  R_delta_key='r500c')

add_derived_field('Mg_bulk/Mg_all_200m',function=_bulk_all_ratio_profile,
                  combine_function=calculate_bulk_all_ratio_profile, 
                  R_delta_key='r200m')

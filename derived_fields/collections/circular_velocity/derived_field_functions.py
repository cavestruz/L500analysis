'''Derive the circular velocity profile: GM(R)/R'''

from L500analysis.derived_fields.derived_fields import *
from L500analysis.derived_fields.derived_field_functions import *
from L500analysis.plotting.profiles.tools.make_profile import make_profile
from L500analysis.utils.constants import kpc2cm, Msun2g, gravc, cm2km

def _normalized_circular_velocity_squared(data,*args,**kwargs) :    
    
    Mtot={hid: data.profiles['M_dark'][hid] + \
              data.profiles['M_gas'][hid] + \
              data.profiles['M_star'][hid] \
              for hid in data.halo_ids}

    Rmid = data.profiles['r_mid']
    Rvir = data.halo_properties[kwargs['R_delta_key']]
    Mvir = data.halo_properties[kwargs['M_delta_key']]
    Rscaled = {hid: Rmid[hid]/Rvir[hid] for hid in data.halo_ids}

    return dict({'M_tot':Mtot, 'Rmid':Rmid, 'Rvir':Rvir, 
                 'Mvir':Mvir, 'Rscaled':Rscaled, 
                 'halo_ids':data.halo_ids},
                **kwargs)
    

def calculate_vcirc2(mass_Msun=None, radius_kpc=None) :
    '''(km/s)^2'''

    radius_cm = radius_kpc * kpc2cm
    mass_g = mass_Msun * Msun2g

    return gravc * mass_g / radius_cm * cm2km**2


def calculate_circular_velocity_squared(input_data) :
    
    d = input_data 
    vcirc_squared = {}
    for hid in d['halo_ids'] :
        vcirc_squared[hid] = calculate_vcirc2(mass_Msun=d['M_tot'][hid],
                                             radius_kpc=d['Rmid'][hid])
        vcirc_squared[hid] = make_profile(x=d['Rscaled'][hid],
                                          y=vcirc_squared[hid])
    return vcirc_squared

def calculate_normalized_circular_velocity_squared(input_data) :

    d = input_data
    Vc2 = calculate_circular_velocity_squared(d) 
    Vc2vir = {hid: Vc2[hid]/calculate_vcirc2(mass_Msun=d['Mvir'][hid], 
                                             radius_kpc=d['Rvir'][hid]) 
              for hid in d['halo_ids']}
    return Vc2vir
                                             
                                             

add_derived_field('Vcirc2_200m',function=_normalized_circular_velocity_squared,
                  combine_function=calculate_circular_velocity_squared,
                  R_delta_key='r200m',
                  delta='200m')

add_derived_field('Vcirc2_500c',function=_normalized_circular_velocity_squared,
                  combine_function=calculate_circular_velocity_squared,
                  R_delta_key='r500c',
                  delta='500c')

add_derived_field('Vcirc2_Vc200m',function=_normalized_circular_velocity_squared,
                  combine_function=calculate_normalized_circular_velocity_squared,
                  R_delta_key='r200m',
                  M_delta_key='M_total_200m')

add_derived_field('Vcirc2_Vc500c',function=_normalized_circular_velocity_squared,
                  combine_function=calculate_normalized_circular_velocity_squared,
                  R_delta_key='r500c',
                  M_delta_key='M_total_500c')
        

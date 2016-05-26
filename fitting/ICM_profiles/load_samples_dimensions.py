'''Load profile, normalization, radii, radial normalization, peak
height, and redshift'''

from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.plotting.profiles.T_evolution.Tmw_evolution.derived_field_functions\
    import *


aexps = [1.0]#,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]

profiles_list = ['T_mw', 'r_mid',
                 'T_mw/T200m',
                 'R/R200m']

halo_properties_list=['r200m','M_total_200m','nu_200m']

db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

def load_sample() :
    for aexp in aexps :
        cldata = GetClusterData(aexp=aexp,db_name=db_name,
                                db_dir=db_dir,
                                profiles_list=profiles_list,
                                halo_properties_list=halo_properties_list)
    return cldata

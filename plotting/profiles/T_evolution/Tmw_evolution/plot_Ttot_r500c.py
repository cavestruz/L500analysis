from L500analysis.data_io.get_cluster_data import GetClusterData
from derived_field_functions import *

aexps = [1.0]
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['T_mw', 'r_mid', 
                 'vel_gas_rad_std', 'vel_gas_tan_std',
                 'vel_gas_rad_avg', 'vel_gas_tan_avg',
                 'Tnt/T500c','Ttot/T500c',#,'T_mw/T500c',
                 'R/R500c']

halo_properties_list=['r500c','M_total_500c']


for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)
    hid = cldata['halo_ids'][0]

    print 'R/R500c:', cldata['R/R500c'][hid]
    print 'Tnt/T500c', max(cldata['Tnt/T500c'][hid])

from L500analysis.data_io.get_cluster_data import GetClusterData
from derived_field_functions import *

aexps = [1.0]
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'
profiles_list = ['M_dark', 'M_gas', 'M_star','M_tot', 'r_mid', 'R/R500c']
halo_properties_list=['r500c']


for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)
    hid = cldata['halo_ids'][0]

    print 'M_gas:', cldata['M_gas'][hid]
    print 'M_dark:', cldata['M_dark'][hid]
    print 'M_tot:', cldata['M_tot'][hid]
    print 'R/R500c:', cldata['R/R500c'][hid]


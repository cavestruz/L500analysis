from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.utils.constants import rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['r_mid', 'r_in', 'r_out',
                 'M_gas_bin',
                 'rhog_all/rho500c',
                 'R/R500c']

halo_properties_list=['r500c']


rhoratio=r"$\tilde{\rho}=\rho_{gas}/\rho_{500c}$"
frhoz1=r"$\tilde{\rho}/\tilde{\rho}(z=1)$"

pa = PlotAxes(figname='rho_r500c',
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[rhoratio,frhoz1],
              ylog=[True,False],
              xlabel=r"$R/R_{500c}$",
              xlim=(0.2,5),
              ylims=[(1e-1,1e3),(0.6,1.4)])

rho={}
rhoplots = [rho]
clkeys = ['rhog_all/rho500c']
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    rho[aexp] = calculate_profiles_mean_variance(cldata['rhog_all/rho500c'])
    
    pa.axes[rhoratio].plot( rbins, rho[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))

    
for aexp in aexps :
    for rho,ls in zip(rhoplots,linestyles) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=rho[aexp]['mean'],
            var_profile1=rho[aexp]['var'],
            mean_profile2=rho[0.5]['mean'],
            var_profile2=rho[0.5]['var'],
        )


        pa.axes[frhoz1].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls=ls) 
                                                 

pa.axes[rhoratio].tick_params(labelsize=12)
pa.axes[rhoratio].tick_params(labelsize=12)
pa.axes[frhoz1].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=rhoratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=rhoratio)

pa.savefig()

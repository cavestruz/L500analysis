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

profiles_list = ['T_mw', 'r_mid', 
                 'vel_gas_rad_std', 'vel_gas_tan_std',
                 'vel_gas_rad_avg', 'vel_gas_tan_avg',
                 'Tnt/T200m',
                 'R/R200m','fTnt_200m']

halo_properties_list=['r200m','M_total_200m','nu_200m']


Tratio=r"$f_{nt}=T_{nt}/T_{tot}$"
fTz0=r"$f_{nt}/f_{nt}(z=1)$"

pa = PlotAxes(figname='fnt_r200m',
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Tratio,fTz0],
              xlabel=r"$R/R_{200m}$",
              xlim=(0.2,2),
              ylims=[(0.1,1.19),(0.6,1.4)])

Tmw={}
Tplots = [Tmw]
clkeys = ['fTnt_200m']
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    for Tplot, key in zip(Tplots,clkeys) :
        Tplot[aexp] = calculate_profiles_mean_variance(cldata[key])

    pa.axes[Tratio].plot( rbins, Tmw[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))



    
for aexp in aexps :
    for T,ls in zip(Tplots,linestyles) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=T[aexp]['mean'],
            var_profile1=T[aexp]['var'],
            mean_profile2=T[0.5]['mean'],
            var_profile2=T[0.5]['var'],
        )


        pa.axes[fTz0].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls=ls) 
                                                 

pa.axes[Tratio].tick_params(labelsize=12)
pa.axes[Tratio].tick_params(labelsize=12)
pa.axes[fTz0].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=Tratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Tratio)

pa.savefig()

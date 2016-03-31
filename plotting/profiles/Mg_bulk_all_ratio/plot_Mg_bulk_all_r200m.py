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
                 'M_gas_bin','M_gas_bulk_bin',
                 'Mg_bulk/Mg_all_200m',
                 'R/R200m']

halo_properties_list=['r200m']


Mgratio=r"$\tilde{M}=M_{g,bulk}/M_{g,all}$"
fMgz1=r"$\tilde{M}/\tilde{M}(z=1)$"

pa = PlotAxes(figname='Mg_r200m',
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Mgratio,fMgz1],
              ylog=[False,False],
              xlabel=r"$R/R_{200m}$",
              xlim=(0.2,2),
              ylims=[(0.31,1),(0.6,1.4)])

Mg={}
Mgplots = [Mg]
clkeys = ['Mg_bulk/Mg_all_200m']
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    Mg[aexp] = calculate_profiles_mean_variance(cldata['Mg_bulk/Mg_all_200m'])
    
    pa.axes[Mgratio].plot( rbins, Mg[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))

    
for aexp in aexps :
    for Mg,ls in zip(Mgplots,linestyles) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=Mg[aexp]['mean'],
            var_profile1=Mg[aexp]['var'],
            mean_profile2=Mg[0.5]['mean'],
            var_profile2=Mg[0.5]['var'],
        )


        pa.axes[fMgz1].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls=ls) 
                                                 

pa.axes[Mgratio].tick_params(labelsize=12)
pa.axes[Mgratio].tick_params(labelsize=12)
pa.axes[fMgz1].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=Mgratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Mgratio)

pa.savefig()

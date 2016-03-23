from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.plotting.profiles.tools.select_profiles \
    import nu_cut, prune_dict
from L500analysis.utils.constants import linear_rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
nu_threshold = {0:[1.3,2.],1:[2.,2.5],2:[2.5,3.6]}# 1.3, 2, 2.5, 3.6                      
nu_threshold_key = 2
nu_label = r"%0.1f$\leq\nu_{200m}\leq$%0.1f"%(nu_threshold[nu_threshold_key][0],
                                              nu_threshold[nu_threshold_key][1])
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['r_mid', 
                 'R/R200m',
                 'vel_gas_rad_avg',
                 'vel_dark_rad_avg',
                 'bulk_vel_gas_rad_avg',
                 'VrVc_ratio_200m',
                 ]

halo_properties_list=['r200m','M_total_200m','nu_200m']


Vratio=r"$\tilde{V}=1-V_r/V_{circ,200m}$"
fVz1=r"$\tilde{V}/\tilde{V}(z=1)$"

pa = PlotAxes(figname='Vall_r200m_nu%01d'%nu_threshold_key,
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Vratio,fVz1],
              ylog=[False,False],
              xlabel=r"$R/R_{200m}$",
              xlim=(0.2,2),
              ylims=[(0.81,2.),(.6,1.39)])

Vr={}
Vplots = [Vr]
clkeys = ['VrVc_ratio_200m']
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    nu_cut_hids = nu_cut(nu=cldata['nu_200m'], threshold=nu_threshold[nu_threshold_key])

    for Vplot, key in zip(Vplots,clkeys) :
        pruned_profiles = prune_dict(d=cldata[key],k=nu_cut_hids)
        Vplot[aexp] = calculate_profiles_mean_variance(pruned_profiles)

    print Vr[aexp]['mean']
    pa.axes[Vratio].plot( linear_rbins, Vr[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))


    
for aexp in aexps :
    for V,ls in zip(Vplots,linestyles) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=V[aexp]['mean'],
            var_profile1=V[aexp]['var'],
            mean_profile2=V[0.5]['mean'],
            var_profile2=V[0.5]['var'],
        )


        pa.axes[fVz1].plot( linear_rbins, fractional_evolution['mean'],
                            color=color(aexp),ls=ls) 
                                                 
pa.axes[Vratio].text(0.2,1.9,nu_label)
pa.axes[Vratio].tick_params(labelsize=12)
pa.axes[Vratio].tick_params(labelsize=12)
pa.axes[fVz1].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=Vratio,ncol=3,loc='lower right', frameon=False)
pa.color_legend_texts(axes_label=Vratio)

pa.savefig()

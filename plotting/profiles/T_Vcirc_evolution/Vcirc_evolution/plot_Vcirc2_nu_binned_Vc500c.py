from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.plotting.profiles.tools.select_profiles \
    import nu_cut, prune_dict
from L500analysis.utils.constants import rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
nu_threshold = [2.3,2.7]
nu_label = r"%0.1f$\leq\nu_{500c}\leq$%0.1f"%(nu_threshold[0],nu_threshold[1])
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['r_mid', 
                 'Vcirc2_Vc500c',
                 'M_dark', 'M_star', 'M_gas',
                 'R/R500c']

halo_properties_list=['r500c','M_total_500c','nu_500c']


Vcirc2ratioVc500c=r"$\tilde{V}=V^2_{c}/V^2_{c,500c}$"
fVcz1=r"$\tilde{V}/\tilde{V}(z=1)$"

pa = PlotAxes(figname='Vcirc2_Vc500c_nu%0.1f'%nu_threshold[0],
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Vcirc2ratioVc500c,fVcz1],
              xlabel=r"$R/R_{500c}$",
              xlim=(0.2,5),
              ylims=[(0.6,1.4),(0.6,1.4)])

Vcirc2={}
clkeys = ['Vcirc2_Vc500c']
plots = [Vcirc2]
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)
    
    nu_cut_hids = nu_cut(nu=cldata['nu_500c'], threshold=nu_threshold)

    for plot, key in zip(plots,clkeys) :
        pruned_profiles = prune_dict(d=cldata[key],k=nu_cut_hids)
        plot[aexp] = calculate_profiles_mean_variance(pruned_profiles)
    
    pa.axes[Vcirc2ratioVc500c].plot( rbins, Vcirc2[aexp]['mean'],color=color(aexp),
                                     ls='-',label="$z=%3.1f$" % aexp2redshift(aexp))


pa.axes[Vcirc2ratioVc500c].fill_between(rbins, Vcirc2[0.5]['down'], Vcirc2[0.5]['up'], 
                                 color=color(0.5), zorder=0)

    
for aexp in aexps :
    for V,ls in zip(plots,linestyles) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=V[aexp]['mean'],
            var_profile1=V[aexp]['var'],
            mean_profile2=V[0.5]['mean'],
            var_profile2=V[0.5]['var'],
            )

        pa.axes[fVcz1].plot( rbins, fractional_evolution['mean'],
                             color=color(aexp),ls=ls) 
                                                 

pa.axes[Vcirc2ratioVc500c].annotate(nu_label, xy=(.75, .75), xytext=(.3, 1.3))
pa.axes[Vcirc2ratioVc500c].tick_params(labelsize=12)
pa.axes[Vcirc2ratioVc500c].tick_params(labelsize=12)
pa.axes[fVcz1].set_yticks(arange(0.6,1.4,0.2))

matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
pa.set_legend(axes_label=Vcirc2ratioVc500c,ncol=3,loc='upper right', frameon=False)
pa.color_legend_texts(axes_label=Vcirc2ratioVc500c)

pa.savefig()

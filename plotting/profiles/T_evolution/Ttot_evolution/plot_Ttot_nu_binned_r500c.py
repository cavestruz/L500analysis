from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.plotting.profiles.tools.select_profiles \
    import *
from L500analysis.utils.constants import rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
nu_threshold = [2.,2.3]
nu_label = r"%0.1f$\leq\nu_{500c}\leq$%0.1f"%(nu_threshold[0],nu_threshold[1])
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['T_mw', 'r_mid', 
                 'vel_gas_rad_std', 'vel_gas_tan_std',
                 'vel_gas_rad_avg', 'vel_gas_tan_avg',
                 'Ttot/T500c',
                 'R/R500c']

halo_properties_list=['r500c','M_total_500c','nu_500c']


Tratio=r"$\tilde{T}=T(R)/T_{500c}$"
fTz0=r"$\tilde{T}/\tilde{T}(z=1)$"

pa = PlotAxes(figname='Ttot_r500c_nu%0.1f'%nu_threshold[0],
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Tratio,fTz0],
              xlabel=r"$R/R_{500c}$",
              xlim=(0.2,5),
              ylims=[(0.1,1.19),(0.6,1.4)])

Tmw={}
Tplots = [Tmw]
clkeys = ['Ttot/T500c']
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    # print aexp
    # print min(cldata['nu_500c'].values())
    # print max(cldata['nu_500c'].values())
    # continue
    nu_cut_hids = nu_cut(nu=cldata['nu_500c'], threshold=nu_threshold)

    for Tplot, key in zip(Tplots,clkeys) :
        pruned_profiles = prune_dict(d=cldata[key],k=nu_cut_hids)
        Tplot[aexp] = calculate_profiles_mean_variance(pruned_profiles)

    pa.axes[Tratio].plot( rbins, Tmw[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))


pa.axes[Tratio].fill_between(rbins, Tmw[0.5]['down'], Tmw[0.5]['up'], 
                                 color=color(0.5), zorder=0)

    
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
                                                 
pa.axes[Tratio].annotate(nu_label, xy=(.75, .75), xytext=(.3, 1.1),
                         )
pa.axes[Tratio].tick_params(labelsize=12)
pa.axes[Tratio].tick_params(labelsize=12)
pa.axes[fTz0].set_yticks(arange(0.6,1.4,0.2))

matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
pa.set_legend(axes_label=Tratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Tratio)

pa.savefig()

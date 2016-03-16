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
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
nu_threshold = [1, 1.7] # 1, 1.7, 2.3, 2.7
nu_label = r"%0.1f$\leq\nu_{500c}\leq$%0.1f"%(nu_threshold[0],nu_threshold[1])
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['T_mw', 'r_mid', 
                 'vel_gas_rad_std', 'vel_gas_tan_std',
                 'vel_gas_rad_avg', 'vel_gas_tan_avg',
                 'M_dark', 'M_star', 'M_gas',
                 'Tmw_Vcirc2_ratio_500c',
                 'R/R500c']

halo_properties_list=['r500c','M_total_500c','nu_500c']


Tmw_Vcirc2_ratio=r"$\Xi=T_{mw}/V^2_{circ}$"
fXz1=r"$\Xi/\Xi(z=1)$"

pa = PlotAxes(figname='Tmw_Vcirc2_ratio_500c_nu%0.1f'%nu_threshold[0],
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Tmw_Vcirc2_ratio,fXz1],
              xlabel=r"$R/R_{500c}$",
              xlim=(0.2,5),
              ylims=[(0.,0.8),(0.6,1.4)])

TratioV2={}
plots=[TratioV2]
clkeys=['Tmw_Vcirc2_ratio_500c']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)
    
    nu_cut_hids = nu_cut(nu=cldata['nu_500c'], threshold=nu_threshold)

    for p, key in zip(plots,clkeys) :
        pruned_profiles = prune_dict(d=cldata[key],k=nu_cut_hids)
        p[aexp] = calculate_profiles_mean_variance(pruned_profiles)

    pa.axes[Tmw_Vcirc2_ratio].plot( rbins, TratioV2[aexp]['mean'],
                                     color=color(aexp),ls='-',
                                     label="$z=%3.1f$" % aexp2redshift(aexp))


pa.axes[Tmw_Vcirc2_ratio].fill_between(rbins, TratioV2[0.5]['down'], 
                                        TratioV2[0.5]['up'], 
                                        color=color(0.5), zorder=0)

    
for aexp in aexps :

    fractional_evolution = get_profiles_division_mean_variance(
        mean_profile1=p[aexp]['mean'],
        var_profile1=p[aexp]['var'],
        mean_profile2=p[0.5]['mean'],
        var_profile2=p[0.5]['var'],
        )

    pa.axes[fXz1].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls='-') 
                                                 
pa.axes[Tmw_Vcirc2_ratio].annotate(nu_label, xy=(.75, .75), xytext=(.3,.7),
                         )
pa.axes[Tmw_Vcirc2_ratio].tick_params(labelsize=12)
pa.axes[Tmw_Vcirc2_ratio].tick_params(labelsize=12)
pa.axes[fXz1].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=Tmw_Vcirc2_ratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Tmw_Vcirc2_ratio)

pa.savefig()

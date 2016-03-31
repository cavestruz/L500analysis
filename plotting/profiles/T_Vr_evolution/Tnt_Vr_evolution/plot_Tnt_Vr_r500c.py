from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.utils.constants import rbins, linear_rbins
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
                 'Tnt_cm_per_s_2_r500c',
                 'Vr2_cm_per_s_2_r500c',
                 'R/R500c']

halo_properties_list=['r500c','M_total_500c']


Tnt_Vr2_ratio=r"$\Xi=T_{nt}/V^2_{r}$"
fXz1=r"$\Xi/\Xi(z=1)$"

pa = PlotAxes(figname='Tnt_Vr2_ratio_500c',
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Tnt_Vr2_ratio,fXz1],
              xlabel=r"$R/R_{500c}$",
              ylog=[True,False],
              xlim=(0.2,5),
              ylims=[(1e-1,1e2),(0.4,1.6)])

TratioV2={}
plots=[TratioV2]
clkeys=['Tnt_Vr2_ratio_500c']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)
    
    Tnt = calculate_profiles_mean_variance(cldata['Tnt_cm_per_s_2_r500c'])
    Vr2 = calculate_profiles_mean_variance(cldata['Vr2_cm_per_s_2_r500c']) 
    TratioV2[aexp] = get_profiles_division_mean_variance(
        mean_profile1=Tnt['mean'], var_profile1=Tnt['var'],
        mean_profile2=Vr2['mean'], var_profile2=Vr2['var'])
        
    print TratioV2[aexp]['mean']
    pa.axes[Tnt_Vr2_ratio].plot( rbins, TratioV2[aexp]['mean'],
                                     color=color(aexp),ls='-',
                                     label="$z=%3.1f$" % aexp2redshift(aexp))
    
for aexp in aexps :
    fractional_evolution = get_profiles_division_mean_variance(
        mean_profile1=TratioV2[aexp]['mean'],
        var_profile1=TratioV2[aexp]['var'],
        mean_profile2=TratioV2[0.5]['mean'],
        var_profile2=TratioV2[0.5]['var'],
        )

    pa.axes[fXz1].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls='-') 
                                                 

pa.axes[Tnt_Vr2_ratio].tick_params(labelsize=12)
pa.axes[Tnt_Vr2_ratio].tick_params(labelsize=12)
pa.axes[fXz1].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=Tnt_Vr2_ratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Tnt_Vr2_ratio)

pa.savefig()

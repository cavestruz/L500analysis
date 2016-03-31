from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.plotting.profiles.tools.select_profiles \
    import nu_cut, prune_dict
from L500analysis.utils.constants import rbins, linear_rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
nu_threshold = {0:[1.3,2.],1:[2.,2.5],2:[2.5,3.6]}# 1.3, 2, 2.5, 3.6                     
nu_threshold_key = 0
nu_label = r"%0.1f$\leq\nu_{200m}\leq$%0.1f"%(nu_threshold[nu_threshold_key][0],
                                              nu_threshold[nu_threshold_key][1])
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['T_mw', 'r_mid', 
                 'vel_gas_rad_std', 'vel_gas_tan_std',
                 'vel_gas_rad_avg', 'vel_gas_tan_avg',
                 'Ttot_cm_per_s_2_r200m',
                 'Vr2_cm_per_s_2_r200m',
                 'R/R200m']

halo_properties_list=['r200m','M_total_200m','nu_200m']


Ttot_Vr2_ratio=r"$\Xi=T_{tot}/V^2_{r}$"
fXz1=r"$\Xi/\Xi(z=1)$"

pa = PlotAxes(figname='Ttot_Vr2_ratio_200m_nu%01d'%nu_threshold_key,
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Ttot_Vr2_ratio,fXz1],
              xlabel=r"$R/R_{200m}$",
              ylog=[True,False],
              xlim=(0.2,2),
              ylims=[(1e-1,1e2),(0.4,1.6)])

TratioV2={}
plots=[TratioV2]
clkeys=['Ttot_Vr2_ratio_200m']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)
    
    nu_cut_hids = nu_cut(nu=cldata['nu_200m'], threshold=nu_threshold[nu_threshold_key])

    Ttot = calculate_profiles_mean_variance(prune_dict(d=cldata['Ttot_cm_per_s_2_r200m'],
                                                       k=nu_cut_hids))
    Vr2 = calculate_profiles_mean_variance(prune_dict(d=cldata['Vr2_cm_per_s_2_r200m'],
                                                      k=nu_cut_hids)) 
    TratioV2[aexp] = get_profiles_division_mean_variance(
        mean_profile1=Ttot['mean'], var_profile1=Ttot['var'],
        mean_profile2=Vr2['mean'], var_profile2=Vr2['var'])
        
    pa.axes[Ttot_Vr2_ratio].plot( rbins, TratioV2[aexp]['mean'],
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
                                                 
pa.axes[Ttot_Vr2_ratio].text(0.2,50.,nu_label)
pa.axes[Ttot_Vr2_ratio].tick_params(labelsize=12)
pa.axes[Ttot_Vr2_ratio].tick_params(labelsize=12)
pa.axes[fXz1].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=Ttot_Vr2_ratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Ttot_Vr2_ratio)

pa.savefig()

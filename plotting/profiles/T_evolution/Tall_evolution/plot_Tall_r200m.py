from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.utils.constants import rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
aexps = [1.0,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['T_mw', 'r_mid', 
                 'vel_gas_rad_std', 'vel_gas_tan_std',
                 'vel_gas_rad_avg', 'vel_gas_tan_avg',
                 'Tnt/T200m','Ttot/T200m','T_mw/T200m',
                 'R/R200m']

halo_properties_list=['r200m','M_total_200m','nu_200m']


Tratio=r"$\tilde{T}=T(R)/T_{200m}$"
fTz0=r"$\tilde{T}/\tilde{T}(z=0)$"

pa = PlotAxes(figname='Tall_r200m',
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Tratio,fTz0],
              xlabel=r"$R/R_{200m}$",
              xlim=(0.2,2.0),
              ylims=[(0.1,1.1),(0.8,1.55)])

Tmw={}
Tnt={}
Ttot={}

Tmw_frac={}
Tnt_frac={}
Ttot_frac={}


for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    Tmw[aexp] = calculate_profiles_mean_variance(cldata['T_mw/T200m'])
    Tnt[aexp] = calculate_profiles_mean_variance(cldata['Tnt/T200m'])
    Ttot[aexp] = calculate_profiles_mean_variance(cldata['Ttot/T200m'])

    pa.axes[Tratio].plot( rbins, Tmw[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))
    pa.axes[Tratio].plot( rbins, Tnt[aexp]['mean'],color=color(aexp),ls='-.' )
    pa.axes[Tratio].plot( rbins, Ttot[aexp]['mean'],color=color(aexp),ls=':' )

    
for aexp in aexps[1:] :
    for T,ls in zip([Tmw, Tnt, Ttot],['-','-.',':']) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=T[aexp]['mean'],
            var_profile1=T[aexp]['var'],
            mean_profile2=T[1.0]['mean'],
            var_profile2=T[1.0]['var'],
        )


        pa.axes[fTz0].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls=ls ) 
                                                 

pa.axes[Tratio].legend(ncol=2,loc='best', frameon=False)
pa.savefig()

from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift,redshift2aexp
from L500analysis.plotting.tools.figure_formatting import *
from L500analysis.plotting.profiles.tools.profiles_percentile \
    import *
from L500analysis.utils.constants import rbins
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
aexps = [1.0,redshift2aexp(0.3),redshift2aexp(0.5),redshift2aexp(0.7),redshift2aexp(0.85),redshift2aexp(1.0)]
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['T_mw', 'r_mid', 
                 'M_gas', 'M_dark', 'M_star',
                 'T_mw/T200m',
                 'T_mw/T500m',
                 'T_mw/T1600m',                 
                 'R/R200m',
                 'R/R500m',
                 'R/R1600m',
                 ]

halo_properties_list=['r200m','M_total_200m']


fTz200m=r"$\tilde{T}_{200m}/\tilde{T}(z=0)$"
fTz500m=r"$\tilde{T}_{500m}/\tilde{T}(z=0)$"
fTz1600m=r"$\tilde{T}_{1600m}/\tilde{T}(z=0)$"
axes_labels = [fTz200m,fTz500m,fTz1600m]
text_xlocs = [.125,0.2,0.2]
pa = PlotAxes(figname='fTmw_deltam',use_axes_labels=False,
              axes=[[0.15,0.65,0.80,0.2],[0.15,0.4,0.80,0.2],[0.15,0.15,0.80,0.2]],
              axes_labels=axes_labels,
              xlabel=r"$R/R_{\Delta}$",
              xlims=[(0.06,0.94),(0.1,1.39),(0.01,2.49)],
              ylims=[(0.8,1.4),(0.8,1.4),(0.8,1.4)])
fT1 = {}
fT2 = {}
fT3 = {}
Tplots = [fT1, fT2, fT3]
deltas = ['200m','500m','1600m']
clkeys = ['T_mw/T'+delta for delta in deltas]
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    # Collect average profiles at each z
    for Tplot, clkey in zip(Tplots,clkeys) :
        Tplot[aexp] = calculate_profiles_mean_variance(cldata[clkey])

for aexp in aexps :
    for T, axes_label in zip(Tplots,axes_labels) :
        fractional_evolution = get_profiles_division_mean_variance(
            mean_profile1=T[aexp]['mean'],
            var_profile1=T[aexp]['var'],
            mean_profile2=T[1.0]['mean'],
            var_profile2=T[1.0]['var'],
        )


        pa.axes[axes_label].plot( rbins, fractional_evolution['mean'],
                            color=color(aexp),ls='-',label="$z=%3.1f$" % aexp2redshift(aexp)) 
                                                 



for axes_label,delta,xloc in zip(axes_labels,deltas,text_xlocs) :
    print axes_label, delta
    pa.axes[axes_label].tick_params(labelsize=12)
    pa.axes[axes_label].set_yticks(arange(0.8,1.4,0.2))
    pa.axes[axes_label].text(xloc,1.2,'$\\Delta='+delta+'$')

pa.axes[axes_labels[1]].set_ylabel("$\\tilde{T}_{\\Delta}/\\tilde{T}(z=0)$",
                                   fontsize="xx-large")
pa.set_legend(axes_label=axes_labels[0],ncol=3,loc='upper right', frameon=False)
pa.color_legend_texts(axes_label=axes_labels[0])

pa.savefig()

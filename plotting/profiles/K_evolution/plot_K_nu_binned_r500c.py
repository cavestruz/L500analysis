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
nu_threshold = {0:[1,1.7],1:[1.7,2.3],2:[2.3, 2.7]} # 1, 1.7, 2.3, 2.7
nu_threshold_key = 0
nu_label = r"%0.1f$\leq\nu_{500c}\leq$%0.1f"%(nu_threshold[nu_threshold_key][0],nu_threshold[nu_threshold_key][1])
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = ['S_mw', 'r_mid', 
                 'S_mw/S500c',
                 'R/R500c']

halo_properties_list=['r500c','M_total_500c','nu_500c']


Sratio=r"$\tilde{K}=K(R)/K_{500c}$"
fSz1=r"$\tilde{K}/\tilde{K}(z=1)$"

pa = PlotAxes(figname='Kmw_r500c_nu%01d'%nu_threshold_key,
              axes=[[0.15,0.4,0.80,0.55],[0.15,0.15,0.80,0.24]],
              axes_labels=[Sratio,fSz1],
              xlabel=r"$R/R_{500c}$",
              ylog=[True,False],
              xlim=(0.2,5),
              ylims=[(0.1,10.1),(0.6,1.4)])

Smw={}
linestyles = ['-']

for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    nu_cut_hids = nu_cut(nu=cldata['nu_500c'], threshold=nu_threshold[nu_threshold_key])

    pruned_profiles = prune_dict(d=cldata['S_mw/S500c'],k=nu_cut_hids)
    Smw[aexp] = calculate_profiles_mean_variance(pruned_profiles)

    pa.axes[Sratio].plot( rbins, Smw[aexp]['mean'],color=color(aexp),ls='-',
                             label="$z=%3.1f$" % aexp2redshift(aexp))


for aexp in aexps :
    fractional_evolution = get_profiles_division_mean_variance(
        mean_profile1=Smw[aexp]['mean'],
        var_profile1=Smw[aexp]['var'],
        mean_profile2=Smw[0.5]['mean'],
        var_profile2=Smw[0.5]['var'],
        )


    pa.axes[fSz1].plot( rbins, fractional_evolution['mean'],
                        color=color(aexp),ls='-') 
                                                 
pa.axes[Sratio].tick_params(labelsize=12)
pa.axes[Sratio].tick_params(labelsize=12)
pa.axes[fSz1].set_yticks(arange(0.6,1.4,0.2))

matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
pa.set_legend(axes_label=Sratio,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=Sratio)
pa.axes[Sratio].annotate(nu_label, xy=(.3, 2.5), xytext=(.3, 6.),
                         )

pa.savefig()

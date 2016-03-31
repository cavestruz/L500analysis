from L500analysis.data_io.get_cluster_data import GetClusterData
from L500analysis.utils.utils import aexp2redshift
from L500analysis.plotting.tools.figure_formatting import *
from derived_field_functions import *

color = matplotlib.cm.afmhot_r
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1
matplotlib.rcParams['legend.fontsize'] = 12
aexps = [1.0,0.9,0.8,0.7,0.6,0.5,0.45,0.4,0.35]
db_name = 'L500_NR_0'
db_dir = '/home/babyostrich/Documents/Repos/L500analysis/'

profiles_list = []

halo_properties_list=['r500c','M_total_500c','nu_500c']


nu=r"$\nu_{500c}$"

pa = PlotAxes(figname='nu_Mtot_500c',
              axes=[[0.18,0.18,0.80,0.80]],
              axes_labels=[nu],
              xlabel=r"$M_{tot,500c}$",
              xlim=(1e12,9.9e15),
              ylims=[(1,4)],
              xlog=[True])


for aexp in aexps :
    cldata = GetClusterData(aexp=aexp,db_name=db_name,
                            db_dir=db_dir,
                            profiles_list=profiles_list,
                            halo_properties_list=halo_properties_list)

    pa.axes[nu].scatter(cldata['M_total_500c'].values(),cldata['nu_500c'].values(), 
                        color=color(aexp),
                        label="$z=%3.1f$" % aexp2redshift(aexp))

for y in [1.,1.7,2.3,2.7] :
    pa.axes[nu].axhline(y=y)

pa.axes[nu].tick_params(labelsize=12)
#pa.axes[nu].set_yticks(arange(0.6,1.4,0.2))
pa.set_legend(axes_label=nu,ncol=3,loc='best', frameon=False)
pa.color_legend_texts(axes_label=nu)

pa.savefig()

#!/usr/bin/python

from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties

from math import fabs

import cart_analysis_db.io.reader as db
import cart_analysis_db.utils.utilities as ut
from cart_analysis_db.utils.non_thermal import calc_pturb


def compute_periodic_distance_1d (z0_halo, halos, boxsize) :
    dxs = {}

    for d in ["x", "y","z"] :
        dxs[d] = []
        for halo in halos :
            dx = z0_halo[d] - halo[d]
            if dx > (boxsize/2.0): dx -= boxsize
            if dx < -(boxsize/2.0): dx += boxsize

            dxs[d].append(dx)

    return dxs    



simulation = "L500_NR_0"

sim = db.Simulation(simulation)
mt = db.Simulation(simulation+"_mt", db_dir=sim.db_dir)


aexp_list = sim.get_halo_epochs()
clusters = mt.get_halo_ids(is_main_halo=True)

property_list = ["x", "y","z","M_hc", "num_particles", "z0_parent_id"]
z0_halos = mt.get_halo_properties(clusters, ["x", "y","z","M_hc"], 1.0005)
halos = mt.get_progenitor_properties(clusters, property_list)
mergers = mt.get_merger_history(clusters, mass_ratio_cut = 1./6.)

num_bins = 99

for z0_halo in z0_halos:
    cluster = z0_halo['id']
    print cluster
    this_halo = halos[halos['z0_parent_id'] == cluster]
    main_mergers = mergers[mergers['z0_parent_id'] == cluster]
    for merger in main_mergers :

        print merger["merger_aexp"], merger["merging_id"],(merger["num_shared_particles"]*1.0)/merger["num_particles"], merger["mass_ratio"]


    dxs = compute_periodic_distance_1d(z0_halo, this_halo, sim.boxsize)
    for d in dxs.keys():
        for i,dx in enumerate(dxs[d]) :
            if i >= len(dxs[d])-1 :
                break
            if fabs(dxs[d][i]-dxs[d][i+1])  > 3.0 :
                print this_halo['aexp'], this_halo


 #   Mhse_500 = []
 #   Mhse_aexp = []


#        #ensure all data loads
#        if halo['aexp'] < 0.3 :
   #         continue

  #      halo_data = sim.get_halo_properties([halo['id']], ["r500c"], halo['aexp'])
  #      if not len(halo_data) :
  #          print "no halo data found for id = %d at aexp = %0.4f" % (halo['id'],halo['aexp'])
  #          continue

#        p_profiles = calc_pturb(sim, halo['aexp'], halo['id'])
#        if p_profiles == 0 :
   #         continue


 #       r500c = halo_data['r500c']
 #       Mhse_aexp.append(halo['aexp'])
 #       Mhse_500.append(np.interp(1.0, p_profiles[0][0:num_bins-1]/r500c,
 #                        p_profiles[1]/p_profiles[5][0:num_bins-1]-1.0))

        
    f = figure( figsize=(4,12) )
    axes(ut.define_axes(3, vertical=True)[2])

    f.gca().plot(this_halo['aexp'], dxs['x'], label="x")
    f.gca().plot(this_halo['aexp'], dxs['y'], label="y")
    f.gca().plot(this_halo['aexp'], dxs['z'], label="z")

    if len(main_mergers) > 0 :
    #    print main_mergers['ratio']
        f.gca().vlines(main_mergers['merger_aexp'], ymin = -10, ymax = 10, lw=main_mergers['mass_ratio'])
    
    f.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
    f.gca().set_ylabel("distance from z0")
    f.gca().set_xlabel("aexp")
    f.gca().set_xlim([0,1])

    
    l = f.gca().legend( loc="lower right", prop = FontProperties( size="small"))
    l.draw_frame(False)

    axes(ut.define_axes(3, vertical=True)[1])

    f.gca().plot(this_halo['aexp'], this_halo['M_hc']/z0_halo['M_hc'])
 
    if len(main_mergers) > 0 :
        f.gca().vlines(main_mergers['merger_aexp'], ymin = 0, ymax = 1.2, lw=main_mergers['mass_ratio'])
    
    f.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
    f.gca().set_ylabel("mass/mass_z0")
    f.gca().set_xlabel("aexp")
    f.gca().set_xlim([0,1])

 #   axes(ut.define_axes(3, vertical=True)[0])

  #  f.gca().plot(Mhse_aexp, Mhse_500)
 
#    if len(main_mergers) > 0 :
 #       f.gca().vlines(main_mergers['merger_aexp'], ymin = 0, ymax = 1.2, lw=main_mergers['mass_ratio'])
    
 #   f.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
 #   f.gca().set_ylabel("hse bias")
 #   f.gca().set_xlabel("aexp")
 #   f.gca().set_xlim([0,1])
 #   f.gca().set_ylim([-1,1])

    f.savefig("images/mergertree_diagnostics_"+str(cluster)+".png", dpi=150 )
 
    f.clf()
    close('all')



sim.close()

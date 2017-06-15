#!/usr/bin/python

from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties

from math import fabs

import cart_analysis_db.db as db
from cart_analysis_db.utilities import ut


def compute_periodic_distance_1d (z0_halo, halos, boxsize) :
    dxs = {}

    for d in ["x", "y","z"] :
        dxs[d] = []
        for halo in halos :
            dx = fabs(z0_halo[d] - halo[d])
            if dx > (boxsize/2.0): dx -= boxsize

            dxs[d].append(dx)

    return dxs    



simulation = "L500_NR_0"

sim = db.Simulation(simulation)
mt = db.Simulation(simulation+"_mt", db_dir=sim.db_dir)


aexp_list = sim.get_halo_epochs()
clusters = sim.get_halo_ids()

property_list = ["x", "y","z","M_hc", "z0_parent_id"]
z0_halos = mt.get_halo_properties(clusters, ["x", "y","z","M_hc"], 1.0005)

#halos = mt.get_progenitor_properties(clusters, property_list)
#mergers = mt.get_merger_history(clusters, merger_ratio_cut = 0.1)

for z0_halo in z0_halos:

    cluster = z0_halo['id']
    print cluster

    tree = mt.get_full_tree(cluster)

    for aexp in aexp_list :
        subtree = tree[tree["aexp"] == aexp]
        for id in subtree["id"]:
            if len(subtree[subtree["id"] == id]) > 1 :
                print "Found issue"
                print subtree[subtree["id"] == id]
                for link in subtree[subtree["id"] == id] :
                    print tree[np.logical_and(tree["id"] == link['parent_id'], tree["aexp"] == link['parent_aexp'])]

        

sim.close()
mt.close()
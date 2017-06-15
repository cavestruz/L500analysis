#!/usr/bin/env python

from caps.io import reader as db

simulation = "L500_NR_tracers"

mt = db.Simulation(simulation)

simdir, hcdir, profilesdir = mt.get_directories()

aexp_list = mt.get_halo_epochs()

for aexp in aexp_list:
    clusters = mt.get_halo_ids(aexp=aexp, main_halos_only=True)
    aexp_str = "%0.4f" % aexp
    output = open(simdir+"/"+hcdir+"/progenitors_a"+aexp_str+".dat","w")
    for cluster in clusters:
        print >>output, cluster
    output.close()

        

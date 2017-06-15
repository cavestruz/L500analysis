#!/usr/bin/env python

import caps.io.reader as db


print "Loading database and executing queries..."

sim = db.Simulation("L500_NR_0")

#print units
sim.print_units(["M_total_200c", "r500c"])

#prints all column names for all properties and profiles tables
sim.print_avail_properties()


#gets all epochs
aexp_list = sim.get_halo_epochs()

for aexp in aexp_list:
    aexp_str = "%0.4f" % aexp
    print aexp_str
    #gest ids for halo at given aexp
    clusters = sim.get_halo_ids(aexp_str, masscut=1e14)

    #gets properties for list of cluster ids and list of halo properties
    #global properties get returned in a numpy structure array so that you can cross section the data anyway you please
    property_list = ["M_total_200c", "r500c"]
    halos = sim.get_halo_properties(clusters, property_list, aexp_str)

    #get property for all halos or subset
    print halos["M_total_200c"]

    massive_halos = halos[halos["M_total_200c"] > 1e15]
    print massive_halos["id"]

    #gets profiles for list of cluster ids and list of halo profiles, id and rmid automatically get returned as well.
    #profiles get returned as dictionary of numpy arrays indexed by property then id. I'm working a way of making this
    #more flexible so you aren't limited to one aexp at a time.
    profiles_list = ["M_dm"]
    profiles = sim.get_halo_profiles(clusters, profiles_list, aexp_str)

    #same for pturb profiles (which are currently in a different table, this may change)
    profiles_list = ["P_vw", "P_rand"]
    pturb_profiles = sim.get_halo_profiles(clusters, profiles_list, aexp_str, table="prand_profiles")

    #get property for one halo at a time
    for id in clusters:
        
        print halos[halos["id"] == id]["r500c"]

        Prand_fraction = pturb_profiles["P_rand"][id]/(pturb_profiles["P_vw"][id]+pturb_profiles["P_rand"][id])



sim.close()

#see io/reader.py for additional functions




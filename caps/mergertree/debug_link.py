#!/usr/bin/python

"""
Script to generate merger tree on the fly
"""

import sys
import math
import numpy as np

from caps.io.constructor import Constructor       

from astropy.cosmology import WMAP5
from operator import itemgetter

aexp_list = [1.0005,0.9764]
choice_clusters = [1]
expected_matches = []

test_np = True

mt_simulation = "L25"
mt_db_dir = "."
restart = False #restart functionality doesnt work yet 
fraction_most_bound = 1.0
masscut = 8.4 #Msol/h
has_main_halos = False
min_halo_particles = 1e4
min_joint_particles = 500
search_distance_multiplier = 3.0

sys.exit("Error: Debug link currently does not work.")

with Constructor(mt_simulation, db_dir=mt_db_dir) as mt:

    print aexp_list

    z0_clusters = mt.get_halo_ids(aexp=aexp_list[0], masscut = masscut, is_main_halo=True, halo_catalog=True)

    for i0 in range(len(aexp_list)-1):

        i1 = i0 + 1 

        parent_aexp = aexp_list[i0]
        child_aexp = aexp_list[i1]

        min_joint_particles0 = min_joint_particles * float(child_aexp)**2

        if parent_aexp == 1.0005:
            phalos = z0_clusters
        if i0 == 0:
            phalos = choice_clusters
            particles_parent = mt.get_particles_from_file(parent_aexp, clusters=phalos)

        print "Finding matches for %0.4f, %0.4f" % (parent_aexp, child_aexp)


        #get halo properties from database
        print str(len(phalos))+" halos identified for matching"
        properties = ["x","y","z", "vx","vy","vz", "M_hc", "r_hc", "num_particles"]
        halos = mt.get_halo_properties(phalos, properties, parent_aexp)

        #load child_particles
        particles_child = mt.get_particles_from_file(child_aexp, min_np = 0)

        links_data = []
        z0id_1 = {}

        #loop through parent halos
        for phalo in choice_clusters:
            halo = halos[halos["id"] == phalo]
            print phalo
            if len(expected_matches) > 0:
                matches = mt.get_halo_properties(expected_matches, properties, child_aexp)
                for match in matches:
                    print match
                    print "x distance: ", halo["x"] - match["x"]
                    print "y distance: ", halo["y"] - match["y"]
                    print "z distance: ", halo["z"] - match["z"]
                    shared_particles = list( set(map(itemgetter(0),particles_parent[phalo]))
                                    & set(map(itemgetter(0),particles_child[match["id"]])) )
                    print "shared particles: ", len(shared_particles )
                    print "mass ratio: ", float(match["M_hc"])/float(halos["M_hc"])

     #       print "Checking cluster,", parent_aexp, phalo

            #determine time difference between the two epochs in seconds
            t1 = WMAP5.age(1./parent_aexp-1.).value
            t2 = WMAP5.age(1./child_aexp-1.).value
            dt = math.fabs(t1 - t2) * 1.0e9 * 3.15569e7 #convert to seconds

            #search cube determined by parent halo velocity + parent halo radius
            pos = np.array([halo["x"], halo["y"], halo["z"]])
            vel = np.array([halo["vx"], halo["vy"], halo["vz"]])
            searchbox = mt.define_searchbox(pos, vel, dt, halo["r_hc"], search_distance = search_distance_multiplier)
            print searchbox

            chalos = mt.get_halos_within_distance(child_aexp,searchbox, [],
                                masscut = 0.01*halo["M_hc"])
            print sorted(chalos)
            
            #loop through satellites within search box
            prog_found = False

            if len(chalos) > 0:

                chalos = chalos["id"]
                z0id = phalo if i0 == 0 else z0id_0[phalo]

                if test_np:
                    this_parent_particles = np.array(map(itemgetter(0),particles_parent[phalo]))
                else:
                    this_parent_particles_set = set(map(itemgetter(0),particles_parent[phalo]))

                #loop through satellites within search box
                for chalo in chalos:

                    if test_np:
                        this_child_particles = np.array(map(itemgetter(0),particles_child[chalo]))
                        shared_particles = np.intersect1d(this_child_particles, this_parent_particles)
                    else:
                        shared_particles = this_parent_particles_set.intersection(map(itemgetter(0),particles_child[chalo]))
                    
                    if len(shared_particles) > min_joint_particles0:

                        if debug:
                            ratio = float(len(particles_child[chalo]))/float(len(particles_parent[phalo]))
                            print "Possible progenitor found: ", chalo, len(shared_particles), ratio

                        links_data.append((parent_aexp, child_aexp, phalo, chalo, len(shared_particles), z0id, 0 ))
                        z0id_1[chalo] = z0id
                        prog_found = True

            if not prog_found:
                print "No matches found for halo "+str(phalo)+" at aexp = "+str(child_aexp)

        particles_parent = particles_child
        z0id_0 = z0id_1
        phalos = z0id_0.keys()




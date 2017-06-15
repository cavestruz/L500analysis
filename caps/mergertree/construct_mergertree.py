#!/usr/bin/python

"""
Script to generate merger tree and input into database
"""

import sys
import math
import logging
import numpy as np

from caps.io.constructor import Constructor
from caps.util import cart_io
from caps.util import utilities as ut

from astropy.cosmology import WMAP5
from operator import itemgetter


#configuration parameters

mt_simulation = "L500_NR_tracers"
mt_db_dir = "."
restart = False #restart functionality doesnt work yet 
fraction_most_bound = 1.0
mass_cut = 5e11 #Msol/h
has_main_halos = True
min_joint_particles_factor = 0.001
search_distance_multiplier = 3.0

do_generate_links = False
do_generate_tracks = False
do_generate_mergers = True

def generate_links(mt, aexp_list, z0_clusters, particles_dir) :
    """Generates links from halo particle data"""

    if restart:
        phalos, last_aexp = mt.restart_mergertree()
        print "restarting merger tree code from %0.4f" % last_aexp
        particles_file = "%s/halo_particles_a%0.4f.dat" % (particles_dir, last_aexp)

    else:
        phalos = z0_clusters
        z0id_0 = dict((phalo, phalo) for phalo in phalos)
        particles_file = "%s/halo_particles_a%0.4f.dat" % (particles_dir, aexp_list[0])
    
    particles_parent = cart_io.read_halo_particles(particles_file, clusters=phalos)

    for i0 in range(len(aexp_list)-1):

        i1 = i0 + 1 
        parent_aexp = aexp_list[i0]
        child_aexp = aexp_list[i1]

        if restart and child_aexp >= last_aexp:
            continue

        t1 = WMAP5.age(1./parent_aexp-1.)
        t2 = WMAP5.age(1./child_aexp-1.)
        dt = math.fabs(t1 - t2) * 1.0e9 * 3.15569e7 #convert to seconds

        print "Finding matches for %0.4f, %0.4f" % (parent_aexp, child_aexp)
        print str(len(phalos))+" halos identified for matching"

        #get halo properties from database
        properties = ["x","y","z", "vx","vy","vz", "M_hc", "r_hc", "num_particles"]
        halos = mt.get_halo_properties(phalos, properties, parent_aexp)

        #load child_particles
        particles_file = "%s/halo_particles_a%0.4f.dat" % (particles_dir, child_aexp)
        particles_child = cart_io.read_halo_particles(particles_file, min_np = 0)

        links_data = []
        z0id_1 = {}
        #loop through parent halos

        for phalo_id in phalos:
            
            phalo = halos[halos["id"] == phalo_id].squeeze()

            logging.debug( "Checking cluster,", parent_aexp, phalo )

            searchbox = ut.define_searchbox(phalo, dt,  mt.boxsize, 
                                            search_distance=search_distance_multiplier)

            chalos = mt.get_halos_within_distance(child_aexp, searchbox, ["x","y","z"],
                            mass_cut = 0.01*phalo["M_hc"])


            prog_found = False
            if not chalos.empty:            

                z0id = z0id_0[phalo_id]

                this_parent_particles_set = set(map(itemgetter(0),particles_parent[phalo_id]))
                min_joint_particles = min_joint_particles_factor * len(this_parent_particles_set)

                #loop through satellites within search box
                for i, chalo in chalos.iterrows():

                    chalo_id = chalo["id"]

                    #consider redoing with np.intersect1d(parent, child)
                    shared_particles = this_parent_particles_set.intersection(map(itemgetter(0),particles_child[chalo_id]))
                
                    if len(shared_particles) > min_joint_particles:

                        ratio = float(len(particles_child[chalo_id]))/float(len(particles_parent[phalo_id])) 
                        logging.debug( "Possible progenitor found: ", chalo_id, len(shared_particles), ratio)

                        distance = ut.distance_between_halos(chalo, phalo, mt.boxsize)

                        links_data.append((parent_aexp, child_aexp, phalo_id, chalo_id, len(shared_particles),
                                           ratio, distance, z0id, 0 ))
                        z0id_1[chalo_id] = z0id
                        prog_found = True

            if not prog_found:
                logging.debug("No matches found for halo "+str(phalo_id)+" at aexp = "+str(child_aexp))
                mt.mark_leaf(parent_aexp, phalo_id)
        
        mt.insert("mergertree", links_data)            
        mt.commit()

        z0id_0 = z0id_1
        phalos = z0id_0.keys()
        particles_parent = particles_child


def generate_tracks(mt, aexp_list, z0_clusters) :
    """tracks most massive progenitors for reach halo"""

    mt.add_column("is_main_line", "BOOLEAN", table="mergertree", default=0)

    properties = ["x", "y", "z", "vx", "vy", "vz", "M_hc", "r_hc", "num_particles"]
    z0_halos = mt.get_halo_properties(z0_clusters, properties, aexp_list[0])

    for cluster in z0_clusters:
        print "Finding progenitor line for z0 id: "+str(cluster)

        tree = mt.get_full_tree(cluster)

        parent = z0_halos[z0_halos["id"] == cluster].squeeze()

        progenitor_line = []

        for i,aexp in enumerate(aexp_list[1:]):

            parent_id = parent["id"]

            progenitors = tree[(tree['aexp'] == aexp) & 
                               (tree['parent_id'] == parent_id)]

            #this can be pandas-ized
            t1 = WMAP5.age(1./aexp_list[i-1]-1.)
            t2 = WMAP5.age(1./aexp_list[i]-1.)
            dt = math.fabs(t1 - t2) * 1.0e9 * 3.15569e7 #convert to seconds
       
            #apply smaller searchbox to exclude far off merger candidates
            searchbox = ut.define_searchbox(parent, dt,  mt.boxsize,
                                            search_distance=1.5)

            #identify most massive progenitor
            if not progenitors.empty :
                main_progenitor = identify_most_massive_progenitor(progenitors, 
                                                                   searchbox=searchbox)
                if main_progenitor is None:
                    break

                mt.mark_main_line(main_progenitor['aexp'], main_progenitor['id'],
                                    parent_id = main_progenitor['parent_id'])
                parent = main_progenitor
                progenitor_line.append(parent["id"])

            else:
                break

        print "end of tree for cluster "+str(cluster)
        print progenitor_line 

        mt.commit()


def generate_mergers(mt, aexp_list, z0_clusters):
    """identifies and stores mergers data"""

    mt.create_mergers_table()

    for cluster in z0_clusters:
        print "Finding mergers for z0 id: "+str(cluster)

        tree = mt.get_full_tree(cluster, get_main_line=True)
        main_progenitors = tree[tree['is_main_line'] == 1]

        for i,aexp in enumerate(aexp_list[1:]):
            main_progenitor = main_progenitors[main_progenitors['aexp'] == aexp].squeeze()

            if main_progenitor.empty:
                logging.debug("reached end of progenitor line")
                break

            progenitors = tree[(tree['parent_id'] == main_progenitor['id']) &
                                (tree['parent_aexp'] == aexp)]

            if len(progenitors.index) >= 2 :
                mergers = identify_mergers(cluster, tree, progenitors, 
                                           main_progenitors, mt.boxsize)
                if len(mergers):  
                    mt.add_to_mergers(mergers)

        logging.debug("end of tree for cluster %d" % cluster)
        mt.commit()


def identify_most_massive_progenitor(progenitors, searchbox = None):

    if searchbox is not None :
        is_in_box = progenitors.apply(ut.in_box, axis=1, args=(searchbox,))
        close_progenitors = progenitors[is_in_box]
    else:
        close_progenitors = progenitors
    
    if close_progenitors.empty :
        logging.debug("No progenitors found at aexp %0.4f" % progenitors.head(1)["aexp"])
        most_massive_progenitor = None

    elif len(close_progenitors.index) == 1 :
        most_massive_progenitor = close_progenitors.squeeze()

    else :
        logging.debug("More than one possible progenitor")
        most_massive_index = close_progenitors["num_shared_particles"].idxmax()
        most_massive_progenitor = close_progenitors.ix[most_massive_index].squeeze()

    return most_massive_progenitor


def calculate_impact_parameter(main_track, p_track, box_size) :

    distance = 0.0
    velocity_diff = 0.0

    dx = np.zeros(3)
    dv = np.zeros(3)

    for i, d in enumerate(["x","y","z"]):

        dx[i] = main_track[d] - p_track[d]
        dv[i] = main_track["v"+d] - p_track["v"+d]

        if  math.fabs(dx[i]) > (box_size/2.0) :
            dx[i] -= box_size

        distance += dx[i]*dx[i]
        velocity_diff += dv[i]*dv[i]

    distance = math.sqrt(distance)
    velocity_diff = math.sqrt(velocity_diff)


    theta = math.acos( (dx[0]*dv[0] + dx[1]*dv[1] + dx[2]*dv[2])
                        / (distance * velocity_diff) )

    return distance * math.sin(theta) * 1000.0 # in kpc/h


def identify_mergers(cluster, tree, progenitors, main_progenitors, boxsize):

    start_aexp = progenitors.head(1)['aexp'].values[0]
    mergers = []

    original_main_progenitor = main_progenitors[main_progenitors["aexp"] == start_aexp].squeeze()

    if original_main_progenitor.empty :
        logging.debug( "no main halo track at aexp ", start_aexp)
        return mergers

    merger_found = True

    for i, progenitor in progenitors.iterrows():

        p_track = progenitor
        main_track = original_main_progenitor

        if p_track['id'] != main_track['id']:

            while (ut.distance_between_halos(p_track, main_track, boxsize)*1000.0 <
                   (p_track["r_hc"]+main_track["r_hc"])):

                logging.debug(main_track)
                logging.debug(p_track)
                logging.debug("distance: ", ut.distance_between_halos(p_track,
                              main_track, boxsize)*1000.)
                logging.debug("limit: ", (p_track["r_hc"]+main_track["r_hc"]))

                p_progenitors = tree[(tree['parent_aexp'] == p_track["aexp"]) &
                                     (tree['parent_id'] == p_track["id"])]

                if not p_progenitors.empty:
 
                    p_track = identify_most_massive_progenitor(p_progenitors)

                    main_track = main_progenitors[main_progenitors["aexp"] == p_track["aexp"]].squeeze()
                    if main_track.empty:
                        logging.debug("end of main halo track")
                        merger_found = False
                        break

                    if p_track["id"] == main_track["id"]:
                        logging.debug( "merger rejoins main halo track")
                        merger_found = False
                        break

                else:
                    logging.debug("no progenitor found for satellite, skipping merger")
                    merger_found = False
                    break


            if merger_found:
                
                mass_ratio = p_track["M_hc"]/main_track["M_hc"]

                impact_parameter = calculate_impact_parameter(main_track, p_track, boxsize)

                this_merger = (cluster, round(p_track['aexp'], 4), main_track['id'],
                               p_track['id'], mass_ratio, impact_parameter, 
                               round(start_aexp,4), progenitor['num_shared_particles'])

                logging.debug( "merger", this_merger)
                mergers.append(this_merger)

    return mergers



def main() :
    """Builds merger tree and writes tree to database"""

    with Constructor(mt_simulation, db_dir=mt_db_dir) as mt:

        aexp_list = mt.get_halo_epochs()
        if has_main_halos :
            z0_clusters = mt.get_halo_ids(aexp=aexp_list[0], main_halos_only=True, halo_catalog=True)
        else :
            z0_clusters = mt.get_halo_ids(aexp=aexp_list[0], mass_cut = mass_cut, halo_catalog=True)

        if do_generate_links:

            mt.create_mergertree_table()

            dirs = mt.get_directories()
            particles_dir =  "%s/%s" % (dirs[0], dirs[1])
            generate_links(mt, aexp_list, z0_clusters, particles_dir)

        if do_generate_tracks:
            generate_tracks(mt, aexp_list, z0_clusters)

        if do_generate_mergers:
            generate_mergers(mt, aexp_list, z0_clusters)


if __name__ == '__main__':
    sys.exit(main())


#!/usr/bin/python

import sys
import pandas as pd

from config import *

from caps.io.constructor import Constructor
from caps.util import derived_quantities as dq
from caps.util import cart_io
import migration
import units

def main() :
    """Builds merger tree and writes tree to database"""

    with Constructor(simulation, db_dir=dirs["db_dir"]) as sim:

        migration.create_units_table(sim)

        migration.generate_simulation_table(sim, simulation)

        hc_dir = dirs["sim_root_dir"]+"/"+dirs["halo_catalog_dir"]
        prof_dir = dirs["sim_root_dir"]+"/"+dirs["profiles_dir"]

        if initial_migration :

            aexp_list = cart_io.read_aexp_list_from_files(hc_dir)
            sim.insert('units', units.halo_catalog_units(hc_radius)) 

            for aexp in aexp_list :
                print aexp
                hc_data = cart_io.load_halo_catalog_data(sim, hc_dir, aexp, h_inverse)
                hc_data["is_main_halo"] = 0

                if aexp == aexp_list[0] and set_main_halos:
                    main_halos = cart_io.read_halo_ids_from_file(dirs["sim_root_dir"]+"/"+cluster_ids_file)
                    hc_data.ix[hc_data["id"].isin(main_halos), "is_main_halo"] = 1

                sim.write_frame_to_database(hc_data, "halos")


        else :

            #add halo global data
            if do_write_halos :
                print "migrating halo catalog"
                aexp_list = cart_io.read_aexp_list_from_files(hc_dir)
                                                         
                hl_aexp_list = cart_io.read_aexp_list_from_files(prof_dir,
                                    filename_prefix="halo_list_"+halo_list_radii[0]+"_a")

                sim.insert('units', units.halo_catalog_units(hc_radius))
                sim.insert('units', units.halo_list_units(halo_list_radii))
                
                for aexp in aexp_list :
                    print aexp
                    hc_data = cart_io.load_halo_catalog_data(sim, hc_dir, aexp, h_inverse)        

                    if aexp in hl_aexp_list :
                        hl_data = cart_io.load_halo_list_data(sim, prof_dir, aexp,
                                                              halo_list_radii, h_inverse)
                        hl_data["is_main_halo"] = 1
                        hc_data = pd.merge(hc_data, hl_data)

                    sim.write_frame_to_database(hc_data, "halos")

            if do_write_profiles :
                #add profiles data
                print "migrating profiles"
                aexp_list = cart_io.read_aexp_list_from_files(prof_dir,
                                            filename_prefix="halo_profile_radius_a")
                sim.insert('units', units.profile_units())

                filename = "%s/%s_a%0.4f.dat" % (prof_dir, "halo_profile_mass", aexp_list[0])
                clump_exclusion = cart_io.check_for_clump_exclusion(filename)
                if clump_exclusion :
                    print "#clump exclusion is ", clump_exclusion
                    sim.insert('simulation', [["clump_threshold", str(clump_exclusion), ""]] )
                
                for aexp in aexp_list :
                    print aexp

                    halo_list = sim.get_halo_ids(aexp=aexp, main_halos_only = True) 

                    profiles = cart_io.load_profiles_data(sim, prof_dir, aexp, 
                                                          h_inverse, halo_list=halo_list)   
                    if isinstance(profiles, pd.DataFrame):

                        dq.calc_all_densities(profiles)
                        dq.calc_total_mass(profiles)
                        dq.calc_prand(profiles)

                        sim.write_frame_to_database(profiles, "profiles")


if __name__ == '__main__':
    sys.exit(main())

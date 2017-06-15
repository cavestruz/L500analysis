#!/usr/bin/python

simulation = "L500_NR_tracers"

dirs = {"sim_root_dir" : "/home/fas/nagai/kln26/group_scratch/L500_NR_tracers",
        "db_dir" : "..",
        "halo_catalog_dir" : "HC.500",
        "profiles_dir" : "profiles",
        "logs_dir" : "logs" }

hc_radius = "500c"
halo_list_radii = ["200m", "500c", "200c", "vir"]

h_inverse = {"in_profiles": True,
          "in_halo_catalog" : True,
          "into_db" : True,
          "h" : 0.7 }

initial_migration = True
set_main_halos = True
cluster_ids_file = "cluster_ids.dat"

do_write_halos = True
do_write_profiles = True

enabled_hydro = True
enabled_star_formation = False
enabled_epnoneq = False

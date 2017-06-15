#!/usr/bin/python

from config import *

def generate_simulation_table(sim, catalog) :

    sim_table_name = "simulation"

    columns = (("quantity", "TEXT"),
                  ("value", "TEXT"),
                  ("notes", "TEXT"))

    sim.create_table(sim_table_name, columns)

    omega_dir = dirs["sim_root_dir"]

    info = (("catalog", catalog,""),
            ("omega_dir", omega_dir, ""),
            ("local_dir", "~/Data",""),
            ("halo_dir",  dirs["halo_catalog_dir"], ""),
            ("profiles_dir",  dirs["profiles_dir"], "") )

    sim.insert(sim_table_name, info)

    info = parse_config_log(omega_dir+"/"+ dirs["logs_dir"])

    sim.insert(sim_table_name, info)

    sim.commit()


def create_units_table(sim):

    columns = (("quantity", "TEXT"),
              ("description", "TEXT"),
              ("units", "TEXT"),
              ("notes", "TEXT"))

    sim.create_table("units", columns)


def parse_config_log(log_dir) :

    f_input = open(log_dir+"/config.log","r")

    headers = ["Cosmological parameter:", "Primary units:",
               "MESH PARAMETERS", "CONTROL PARAMETERS",
               "GLOBAL SETTINGS", "This cosmology is flat"]

    info = []

    end_reached = False

    while 1 :
        line = f_input.readline()
        
        if not line :
            break
        
        line = line.strip()

        if line == "UNITS" :
            if end_reached :
                break
            else:
                end_reached = True


        if line in headers :
            continue

        if line == "Primary settings:":

            primary_settings = []
            line = f_input.readline().strip()

            while "Other settings:" not in line:
                primary_settings.append(line)
                line = f_input.readline().strip()

            info.append(("primary_settings",",".join(primary_settings),""))
            line = f_input.readline().strip()
            if line.startswith("!") or line in headers :
                continue

        if len(line.split()) > 1 :
            cols = line.split(None, 1)
            cols[0] = cols[0].replace("=","")
            if cols[0].endswith(":"):
                cols[0] = cols[0].rstrip(":")
            info.append((cols[0],cols[1],""))

     
    return info

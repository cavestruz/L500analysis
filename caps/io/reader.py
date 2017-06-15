#!/usr/bin/python

"""
Read CART simulation metadata, halo data and profiles from sqlite3 database
"""

# system code
import sqlite3
import os
import sys
import logging

import numpy as np
import pandas as pd

from ..util import utilities as ut


class Simulation(object):
    """
    Database connection
    """

    def __init__(self, simulation, db_dir="", float_type=np.float32):

        self.simulation = simulation
        self.db_dir = db_dir
        self.float_type = float_type

        # connect to database
        self.load_database()

    def __repr__(self):
        return ("Connection to SQLite database %s in %s"
                % (self.simulation, self.db_dir))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    # database interface ###
    def load_database(self):
        """
        connects to database
        """

        db_path = self.get_database_location()

        if os.path.isfile(db_path):
            print "looking in " + self.db_dir + " for " + self.simulation + ".db"
        else:
            print ("Opening database " + db_path + " for first time. "
                   "Creating new database file.")

        try:
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

        except:
            print "Error opening db."
            return False

        self._tell_sqlite_about_numpy()
        self._get_boxsize()

        return True

    def get_database_location(self):

        if self.db_dir == "":
            env = os.environ.get('SIM_ENV')
            if env is None:
                print ("Environmental Variable 'SIM_ENV' not found."
                       "Please set in your .bashrc or .bash_profile "
                       "to your current machine (i.e. 'omega' or 'local')")
                sys.exit(2)

            elif env == "omega":
                dir = "/lustre/scratch/client/fas/nagai/projects"

            elif env == "local":
                dir = os.environ['HOME'] + "/Data"

            else:
                print ("Environmental Variable 'SIM_ENV' not recognized."
                       "Please set in your .bashrc or .bash_profile "
                       "to your current machine (i.e. 'omega' or 'local')")
                sys.exit(2)

            self.db_dir = dir + "/" + self.simulation

        db_path = self.db_dir + "/" + self.simulation + ".db"

        return db_path

    def _tell_sqlite_about_numpy(self):

        for t in (np.int8, np.int16, np.int32, np.int64,
                  np.uint8, np.uint16, np.uint32, np.uint64):
            sqlite3.register_adapter(t, long)
        for f in (np.float, np.float32, np.float64):
            sqlite3.register_adapter(f, float)

    def close(self):
        """
        closes database
        """
        self.conn.close()

    def execute(self, sql_statement):
        """
        executes given query and returns all rows
        sql_statement: valid sqlite3 query
        """

        logging.debug(sql_statement)

        self.cursor.execute(sql_statement)
        result = self.cursor.fetchall()

        logging.debug(str(len(result)) + " records fetched")

        if len(result) < 1:
            logging.warning(
                "No records found matching query: " + sql_statement)
#            sys.exit(1)

        return result

    def execute_one(self, sql_statement):
        """
        executes given query and returns one row
        sql_statement: valid sqlite3 query
        """

        logging.debug(sql_statement)

        self.cursor.execute(sql_statement)
        rows = self.cursor.fetchone()

        logging.debug(str(len(rows)) + " records fetched")

        if len(rows) < 1:
            logging.warning(
                "No records found matching query: " + sql_statement)
#            sys.exit(1)

        return rows

    def execute_df(self, sql_query):
        """
        executes given query and returns pandas dataframe containing the result
        """

        return pd.read_sql(sql_query, self.conn)

    # Retrieval methods ###
    def _get_boxsize(self):
        """
        returns box size of simulation as float
        NOTE: this function is not super robust. Consider
        asking the user to input box size during construction
        """
        try:
            query = "SELECT value from simulation where quantity = 'Box'"
            string = self.execute_one(query)[0]

            string = string.replace("size:", "")
            string = string.replace("CHIMP", "")
            string = string.replace(" ", "")

            self.boxsize = float(string)

        except:
            logging.warning("Box size not defined yet")
            self.boxsize = ""

    def print_avail_properties(self,
            tables=["halos", "profiles","mergertree","mergers"]):
        """
        prints all column names for specified tables
        """

        for table in tables:

            print "Table: " + table
            r = self.execute_one('select * from ' + table)

            print "Available columns: ", r.keys()
            
    def get_avail_properties(self,
                             table=None):
        '''kwarg: table='halos', 'profiles', 'mergertree', ' mergers' '''
        r = self.execute_one('select * from ' + table)
        return r.keys()
            

    def print_units(self, property_list):
        """
        prints descriptions and units for list of column names
        property_list: column names to be requested in list of strings
        """

        property_str = '"%s"' % '", "'.join(map(str, property_list))
        query = "SELECT * FROM units WHERE quantity in (" + property_str + ");"
        rows = self.execute(query)

        for row in rows:
            print "%s: %s [%s] %s" % (row["quantity"],
                                      row["description"],
                                      row["units"],
                                      row["notes"])

    def print_sim_data(self, property_list, table="simulation"):
        """
        prints values and notes for list of simulation configuation parameters
        property_list: column names to be requested in list of strings
        """

        property_str = '"%s"' % '", "'.join(map(str, property_list))
        query = "SELECT * FROM " + self.simulation + \
            " WHERE quantity in " + property_str
        rows = self.execute(query)

        for row in rows:
            if row["notes"]:
                row["notes"] = '(' + row["notes"] + ')'
            print "%s: %s %s" % (row["quantity"], row["value"], row["notes"])

    def get_directories(self):
        """
        returns paths for simulation root directory,
        halo catalog directory and profiles directory
        """

        env = os.environ.get('SIM_ENV')
        if env is None:
            print ("Environmental Variable 'SIM_ENV' not found."
                   "Please set in your .bashrc or .bash_profile"
                   "to your current machine (i.e. 'omega' or 'local')")
            sys.exit(2)

        query = "SELECT value FROM simulation WHERE quantity in ('" + \
            env + \
            "_dir','halo_dir', 'profiles_dir')"

        directories = self.execute(query)

        simdir = directories[0][0]
        hcdir = directories[1][0]
        profilesdir = directories[2][0]

        return os.path.expanduser(simdir), hcdir, profilesdir

    def find_aexp(self, aexp=None, table="halos"):
        """
        returns latest expansion factor
        aexp: expansion factor to search nearby, if set to
        None, closest aexp to 1 will be returned
        """
        if aexp is None:
            aexp = self.execute_one(
                "SELECT aexp FROM " + table + " ORDER BY aexp DESC LIMIT 1")
        else:
            aexp = self.execute_one(
                "SELECT aexp FROM " + table + " ORDER BY ABS("+str(aexp)+" - aexp) ASC LIMIT 1")

        return aexp[0]

    def get_halo_epochs(self, table="halos"):
        """
        returns numpy array of all expansion factors
        """

        rows = self.execute(
            "SELECT DISTINCT aexp FROM " + table + " ORDER BY aexp DESC")

        epochs = np.array(zip(*rows)[0])

        return epochs

    def get_halo_ids(self, aexp=None, mass_cut=0.0, delta="200m",
                     min_halo_particles=0, table="halos",
                     main_halos_only=False, halo_catalog=False):
        """
        returns numpy array of halo ids at specified expansion factor
        aexp: expansion factor
        """

        if aexp is None:
            aexp = self.find_aexp()

        query = "SELECT id FROM " + table + " where aexp=" + str(aexp)

        if main_halos_only:
            query += " and is_main_halo=1"
        if mass_cut > 0.0:
            if halo_catalog:
                query += " and M_hc > " + str(mass_cut)
            else:
                query += " and M_total_" + delta + " > " + str(mass_cut)
        if min_halo_particles > 0:
            query += " and num_particles > " + str(min_halo_particles)

        id_rows = self.execute(query)

        if len(id_rows):
            halo_ids = list(zip(*id_rows)[0])

        else:
            print "No halos found."
            halo_ids = []

        return halo_ids

    def get_progenitor_ids(self, halo_list, table="halos", df=True):
        """
        returns progenitor lines for specified halos
        as a pandas data frame
        halo_list: list of integer halo ids
        """

        halo_str_list = self.list_to_sql_string(halo_list)

        query = "SELECT id, aexp, z0_parent_id FROM " + table
        query += " inner join mergertree on halos.id=mergertree.child_id"
        query += " and halos.aexp=mergertree.child_aexp where"
        query += " is_main_line = 1 and z0_parent_id in " + halo_str_list
        query += " ORDER BY halos.aexp ASC"
    
        if df == True:
            return self.execute_df(query)
        else :
            progenitors = {}
            rows = self.execute(query)
            for id in halo_list :
                progenitors[id] = {}
            for row in rows :
                progenitors[row[2]][row[1]] = row[0]
            return progenitors

    def get_full_tree(self, id, table="mergertree", get_main_line=False):
        """
        returns pandas data frame containing full merger tree
        for specified z=0 halo id
        """

        columns = ("halos.id, aexp, x, y, z, vx, vy, vz, r_hc, M_hc, "
                   "num_particles, parent_aexp, parent_id, "
                   "num_shared_particles")
        if get_main_line:
            columns += ", is_main_line"
        query = "select %s from halos inner join mergertree " % columns
        query += "on halos.id=mergertree.child_id "
        query += "and halos.aexp=mergertree.child_aexp where "
        query += "z0_parent_id=%d ORDER BY parent_aexp DESC" % id

        return self.execute_df(query)

    def get_halo_properties(self, halo_list, property_list, aexp,
                            table="halos",df=True):
        """
        returns halo global properties from halos table
        halo_list: list of integer halo ids
        property_list: column names to be requested in list of strings
        aexp: expansion factor. Note: if not using nparray=True,
        only provide a single aexp
        """

        halo_str_list = self.list_to_sql_string(halo_list)

        property_str = 'id, %s' % ', '.join(map(str, property_list))

        query = "SELECT " + property_str + " FROM " + table + \
            " WHERE aexp = " + str(aexp) + " and id in " + halo_str_list

        if df == False:
            rows = self.execute(query)
            halos = dict([ (property, {}) for property in property_list])
            for row in rows:
                for property in property_list :
                    halos[property][row["id"]] = row[property]

        else :
            halos = self.execute_df(query)

        return halos

    def get_progenitor_properties(self, halo_list_z0, property_list,
                                  aexp_list=None, table="halos", df=True):
        """
        returns halo global properties from halos table
        halo_list_z0: list of integer halo ids at z=0
        property_list: column names to be requested in list of strings
        aexp: expansion factor
        """

        halo_str_list = self.list_to_sql_string(halo_list_z0)

        property_str = 'id, aexp, z0_parent_id, %s' % ', '.join(
            map(str, property_list))

        query = "SELECT " + property_str + " FROM " + table
        query += " inner join mergertree on halos.id=mergertree.parent_id "
        query += "and halos.aexp=mergertree.parent_aexp where "
        query += "is_main_line = 1 and z0_parent_id in " + halo_str_list

        if aexp_list is not None:
            aexp_str_list = self.list_to_sql_string(aexp_list)
            query += " and aexp in " + aexp_str_list
        query += " ORDER BY halos.aexp ASC"

        if df == False:
            rows = self.execute(query)            
            halos = dict([ (property, {}) for property in property_list])
            for row in rows:
                for property in property_list :
                    halos[property][row["id"]] = row[property]

        else :
            halos = self.execute_df(query)

        return halos

    def get_halo_profiles(self, halo_list, profile_list, aexp,
                          table="profiles", df=True):
        """
        returns profiles from specified table
        halo_list: list of integer halo ids
        profile_list: column names to be requested in list of strings
        aexp: expansion factor
        table: database table to be queried
        by_id: if True, returned dictionary will be indexed by id
        then column name, else vice versa
        """

        halo_str_list = self.list_to_sql_string(halo_list)

#       profile_str = 'id, bin, r_mid, %s' % ', '.join(map(str, profile_list))
        profile_str = 'id, r_mid, %s' % ', '.join(map(str, profile_list))

        query = "SELECT " + profile_str + " FROM " + table + " WHERE aexp = "
        query += str(aexp) + " and id in " + halo_str_list
        query += " ORDER BY id, r_mid"

        if df==False :
            rows = self.execute(query)
            profiles = self.restructure_profiles(halo_list, profile_list[:], rows)
            return profiles

        else:
            rows = self.execute_df(query)
            return rows


    def restructure_profiles(self, halo_list, profile_list, rows) :
        '''
        restructures rows returned by query into dictionaries of profiles (as numpy arrays)
        indexed by column name and then by id
        '''

        profiles = dict([ (profile, dict([ (id, []) for id in halo_list ])) for profile in profile_list])
       
        for row in rows :
            for i in range(len(profile_list)) :
                profiles[profile_list[i]][row["id"]].append(row[profile_list[i]])  
        for i in range(len(profile_list)) :
            for id in halo_list :
                profiles[profile_list[i]][id] = np.array(profiles[profile_list[i]][id])

        return profiles

    def get_progenitor_profiles(self, halo_list_z0, profile_list,
                                table="profiles"):

        raise NotImplemented(
            "Cannot yet get progenitor profiles. Coming soon!")

    def get_halos_within_distance(self, aexp, searchbox, property_list, mass_cut=0.0,
                                  table="halos"):
        """
        returns all halos within specified search box above specified mass
        """

        property_str = self.property_list_to_sql_string(property_list, ["id"])

        query = "SELECT " + property_str
        query += " FROM " + table + " where aexp=" + str(aexp)

        for i, d in enumerate(["x", "y", "z"]):

            # check to see if search box spans a box edge
            if searchbox[(2 * i)] > searchbox[(2 * i) + 1]:
                search_parameters = (
                    d, searchbox[(2 * i) + 1], searchbox[(2 * i)])
                query += " and (%s NOT BETWEEN %e AND %e)" % search_parameters

            else:
                search_parameters = (
                    d, searchbox[(2 * i)], searchbox[(2 * i) + 1])
                query += " and (%s BETWEEN %e AND %e)" % search_parameters

        if mass_cut > 0.0:
            query += " and M_hc > %f" % mass_cut

        return self.execute_df(query)

    def get_merger_history(self, halo_list, mass_ratio_cut="", shared_particles_cut=0.1,
                           merger_table="mergers", halo_table="halos"):
        """
        returns full halo track for selected halos, starting at z=0
        """

        halo_str_list = self.list_to_sql_string(halo_list)

        query = "SELECT DISTINCT * FROM " + halo_table + \
            " as h inner join " + merger_table + \
            " as m on h.aexp = m.merger_aexp"
        query += " and h.id = m.merging_id where z0_parent_id in " + \
            halo_str_list

        if mass_ratio_cut:
            query += " and mass_ratio > %e" % mass_ratio_cut
        if shared_particles_cut:
            query += " and (m.num_shared_particles*1.0)/h.num_particles > "
            query += "%e" % shared_particles_cut

        return self.execute_df(query)

    def get_last_major_mergers(self, halo_list, mass_ratio_cut, table="mergers"):
        """
        returns last major merger expansion factor, aexp, from z=0
        halo_list: list of integer halo ids
        mass_ratio_cut: mass ratio for determining major mergers
        """
        halo_str_list = self.list_to_sql_string(halo_list)

        query = "SELECT z0_parent_id, max(merger_aexp), mass_ratio FROM " + \
            table + " where z0_parent_id in " + \
            halo_str_list
        query += " and mass_ratio > %e group by z0_parent_id" % mass_ratio_cut

        mergers = self.execute_df(query)
        mergers.rename(
            columns={"max(merger_aexp)": "merger_aexp"}, inplace=True)
        mergers.rename(columns={"z0_parent_id": "id"}, inplace=True)

        mergers["merger_t"] = mergers[
            "merger_aexp"].apply(ut.calc_age_from_aexp)

        return mergers

    def get_last_major_mergers_alt_aexp(self, halo_list, mass_ratio_cut, aexp, table="mergers"):
        """
        returns last major merger expansion factor, aexp, for non-z=0 outputs
        halo_list: list of integer halo ids
        mass_ratio_cut: mass ratio for determining major mergers
        aexp: expansion factor
        """
        halo_str_list = self.list_to_sql_string(halo_list)

        query = "SELECT z0_parent_id, max(merger_aexp), mass_ratio FROM " + \
            table + " where z0_parent_id in " + \
            halo_str_list
        query += " and mass_ratio > %e group by z0_parent_id" % mass_ratio_cut

        mergers = self.execute_df(query)
        mergers.rename(
            columns={"max(merger_aexp)": "merger_aexp"}, inplace=True)
        mergers.rename(columns={"z0_parent_id": "id"}, inplace=True)

        mergers["merger_t"] = mergers[
            "merger_aexp"].apply(ut.calc_age_from_aexp)

        return mergers

    # Print methods for database #
    def get_units(self, property_list):
        """
        returns units of columns in property_list
        property_list: list of column names
        """

        property_str = '"%s"' % '", "'.join(map(str, property_list))
        query = "SELECT * FROM units WHERE quantity in (" + property_str + ");"
        rows = self.execute(query)

        return rows

    # Methods for reorganizing outputs for easier manipulation ###

    def construct_numpy_array(self, rows):
        '''
        Constructs numpy array from sqlite return
        Note: deprecated now that code relies on pandas
        '''

        if len(rows) < 1:
            logging.debug("length of rows < 1")
            return []

        ft = self.float_type
        column_names = rows[0].keys()
        dtypes = []

        for name in column_names:
            if "id" in name or "particles" in name:
                dtypes.append((name, np.int32))
            elif name in ["is_leaf", "is_main_halo"]:
                dtypes.append((name, np.bool_))
            else:
                dtypes.append((name, ft))

        data_arr = np.zeros(len(rows), dtype=dtypes)

        for i, row in enumerate(rows):
            for name in column_names:

                data_arr[name][i] = row[name]

        return data_arr

    @staticmethod
    def list_to_sql_string(this_list):
        """
        converts python lists into strings that can be inserted into a sql query
        this_list: list-like
        """

        if len(this_list) == 1:
            str_list = "(" + str(this_list[0]) + ")"
        elif len(this_list) > 1:
            str_list = str(tuple(this_list))
        else:
            print "lists needs to have at least one element"

        return str_list

    @staticmethod
    def property_list_to_sql_string(this_list, additional_props):
        """
        converts python lists into strings that can be inserted into a sql query
        this_list: list-like
        additional_props: list-like of additional column names to appended to
        returned list
        """
        this_list += additional_props
        if len(this_list) < 1:
            print "lists needs to have at least one element"
        else:
            str_list = ', '.join(map(str, this_list))

        return str_list

    @staticmethod
    def restructure_profiles_to_panel(rows):
        """
        restructures rows returned by query into a pandas panel
        indexed by column name and then by id
        """

        raise NotImplemented(
            "Cannot yet convert profiles to panels. Coming soon.")

        column_names = rows[0].keys()

        # DOESN'T WORK YET
        profiles = pd.Panel(
            dict((column, rows[column]) for column in column_names))

        return profiles


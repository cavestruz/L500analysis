#!/usr/bin/python

"""
Subclass of Simulation that contains additional methods to construct database.
"""

import sys
import logging

from reader import Simulation


class Constructor(Simulation):

    def commit(self):
        """
        commits database changes
        """

        self.conn.commit()

    def create_table(self, table, initial_columns):
        """
        adds new table to database
        """

        initial_columns_sql = ""

        for i, column in enumerate(initial_columns):
            if i > 0:
                initial_columns_sql += ", "
            initial_columns_sql += column[0] + " " + column[1]

        query = "CREATE TABLE if not exists " + \
            table + " (" + initial_columns_sql + ")"
        self.cursor.execute(query)

    # Database updating methods ###
    def add_column(self, column, type, table="halos", default=""):
        """
        adds new column after checking if it already exists
        """

        query = 'ALTER TABLE ' + table + ' ADD COLUMN ' + column + ' ' + type

        if default != "":
            query += ' DEFAULT ' + str(default)

        try:
            self.cursor.execute(query)
        except:
            logging.warning(
                "column " + column + " already exists in table " + table)
            pass

    def insert(self, table, newdata, all_cols=True, columns="", one_row=False):

        many = True

        if len(newdata) == 0:
            print "Error. No data passed to insert."
            return
        elif len(newdata) == 1 and not one_row:
            newdata = newdata[0]
            holders = ','.join('?' * len(newdata))
            many = False
        elif one_row:
            many = False
            holders = ','.join('?' * len(newdata))
        else:
            holders = ','.join('?' * len(newdata[0]))

        if all_cols:
            query = 'INSERT INTO ' + table + ' VALUES (' + holders + ')'
        else:
            columns_sql = ",".join(columns)
            query = ('INSERT INTO ' + table + 
                     ' (' + columns_sql + ') VALUES (' + holders + ')')

        logging.debug(query)
        logging.debug(newdata)

        if not many:
            self.cursor.execute(query, newdata)
        else:
            self.cursor.executemany(query, newdata)

    def update_rows(self, table, columns, data):

        if len(columns) != len(data[0]) - 2:
            print "mismatched number of columns and number of columns to be updated"
            print len(columns), len(data[0]) - 2

        query = "update " + table + " set "
        for i, column in enumerate(columns):
            if i > 0:
                query += ", "
            query += column + "=?"
        query += "  where aexp=? and id=?"
    
        self.cursor.executemany(query, data)


    def write_frame_to_database(self, data, table, if_exists="append") :

        data.to_sql(table, self.conn, if_exists=if_exists, index=False)

        if table == "halos" :
            self.conn.execute("CREATE INDEX IF NOT EXISTS "
                              "Halo_Index ON halos (aexp, id)")


    def mark_leaf(self, aexp, id, table="mergertree"):
        """
        labels specified halo as a leaf in the merger tree in the database
        """

        query = "update %s set is_leaf=%d where child_aexp=%0.4f and child_id=%d" % (
            table, 1, aexp, id)

        self.cursor.execute(query)

    def mark_main_line(self, aexp, id, parent_id="", table="mergertree"):
        """
        labels specified halo as a main line progenitor in the merger tree in the database
        """

        query = "update %s set is_main_line=%d where child_aexp=%0.4f and child_id=%d" % (
            table, 1, aexp, id)
        if parent_id:
            query += " and parent_id=%d" % parent_id

        self.cursor.execute(query)


        query = "update halos set is_main_halo=%d where aexp=%0.4f and id=%d" % (
                1, aexp, id)

        self.cursor.execute(query)


    def add_to_mergers(self, new_mergers, table="mergers"):
        """
        Adds new data to mergers database table
        """

        self.insert(table, new_mergers)

    def restart_mergertree(self):

        # get list of completed aexp
        query = "SELECT DISTINCT child_aexp FROM mergertree"
        rows = self.execute(query)
        already_done = list(zip(*rows)[0])

        if len(already_done) < 1:
            print "no records in mergertree! remove restart flag in config and try again."
            sys.exit(1)

        # get ids from last completed epoch
        query = "SELECT DISTINCT child_id FROM mergertree WHERE child_aexp = %f;" % already_done[
            -1]
        id_rows = self.execute(query)
        ids = list(zip(*id_rows)[0])

        if len(ids) < 1:
            print "no halos found at aexp %0.4f" % already_done[-1]
            sys.exit(1)

        return ids, already_done[-1]

    # Database table schema ###

    def create_mergertree_table(self):
        """
        schema for mergertree table
        """

        columns = (("parent_aexp", "REAL"),
                   ("child_aexp", "REAL"),
                   ("parent_id", "INTEGER"),
                   ("child_id", "INTEGER"),
                   ("num_shared_particles", "INTEGER"),
                   ("particle_ratio", "REAL"),
                   ("distance", "REAL"),
                   ("z0_parent_id", "INTEGER"),
                   ("is_leaf", "BOOLEAN"))

        self.create_table("mergertree", columns)

    def create_mergers_table(self):
        """
        schema for mergers table
        """

        columns = (("z0_parent_id", "INTEGER"),
                   ("merger_aexp", "REAL"),
                   ("main_line_id", "INTEGER"),
                   ("merging_id", "INTEGER"),
                   ("mass_ratio", "REAL"),
                   ("impact_parameter", "REAL"),
                   ("track_merging_aexp", "REAL"),
                   ("num_shared_particles", "INTEGER"))

        self.create_table("mergers", columns)

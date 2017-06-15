#!/usr/bin/python
 
import unittest
import mock

from pandas.util.testing import assert_frame_equal

import sqlite3

import numpy as np
 
from caps.io import reader

class ConnectionTest(unittest.TestCase):
    """Tests reader's database connection methods"""

    @mock.patch.object(sqlite3, "connect")
    @mock.patch.object(reader.Simulation, "_get_boxsize")
    def test_load_database_and_close(self, get_boxsize, mock_sqlite3):
        mock_sqlite3.return_value = sqlite3.connect(":memory:")
        get_boxsize.return_value = True

        sim = reader.Simulation("L500")

        self.assertTrue(sim is not None)

    @unittest.skip("skipping database location test")
    def test_database_location(self) :
        pass

class ReaderTest(unittest.TestCase):
    """Tests reader"""
     
    @mock.patch.object(reader.Simulation, "load_database")
    @mock.patch.object(reader.Simulation, "_get_boxsize")
    def setUp(self, mock_get_boxsize, mock_load_database,) :

        mock_load_database.return_value = True
        self.sim = reader.Simulation("L500")


    @mock.patch.object(reader.Simulation,'execute')
    def test_boxsize (self, mock_execute):
        """
        test proper handling of failed query of boxsize
        and test successful return and parsing of boxsize
        """
        mock_execute.return_value = []
        self.sim._get_boxsize()
        self.assertEqual(self.sim.boxsize, "")

        mock_execute.return_value = [{'value':'size: 500 CHIMP'}]
        self.sim._get_boxsize()
        mock_execute.assert_called_with("SELECT value from simulation where quantity = 'Box'")
        self.assertTrue(self.sim.boxsize, 500.0)


    @mock.patch.object(reader.Simulation,'execute')    
    def test_get_directories(self, mock_execute):
        mock_execute.return_value = [['/Users/Kaylea/Data/L500'],
                                      ['HC.500'],
                                      ['profiles']]

        result = self.sim.get_directories()

        true_query = "SELECT value FROM simulation WHERE quantity in ('local_dir','halo_dir', 'profiles_dir')"
        mock_execute.assert_called_with(true_query)

        true_result = ("/Users/Kaylea/Data/L500", "HC.500", "profiles")
        self.assertEqual(result, true_result)

    @mock.patch.object(reader.Simulation,'execute_one') 
    def test_find_cluster_aexpn(self, mock_execute):
        #doesn't work because execute called on cursor
        mock_execute.return_value = 1.0005

        result = self.sim.find_aexp()

        true_query = "SELECT aexp FROM halos ORDER BY aexp DESC LIMIT 1"
        mock_execute.assert_called_with(true_query)

        true_result = 1.0005
        self.assertEqual(result, true_result)

    @mock.patch.object(reader.Simulation,'execute')
    @mock.patch.object(reader.Simulation,'find_aexp')
    def test_get_halo_ids(self,  mock_find_aexp, mock_execute,):    
        mock_execute.return_value = [(1,), (2,), (3,)]
        mock_find_aexp.return_value = 1.0005

        true_result = [1, 2, 3]

        #case: use default parameters
        result = self.sim.get_halo_ids()

        true_query = "SELECT id FROM halos where aexp=1.0005"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

        #case: give aexp

        result = self.sim.get_halo_ids(aexp=1.0005)

        true_query = "SELECT id FROM halos where aexp=1.0005"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

        #case: give masscut

        result = self.sim.get_halo_ids(masscut = 1e12)

        true_query = "SELECT id FROM halos where aexp=1.0005 and Mtotal_200m > 1e+12"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

        #case: give alternate delta

        result = self.sim.get_halo_ids(delta = "500c", masscut = 1e12)

        true_query = "SELECT id FROM halos where aexp=1.0005 and Mtotal_500c > 1e+12"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

        #case: halo_catalog = True

        result = self.sim.get_halo_ids(halo_catalog = True, masscut = 1e12)

        true_query = "SELECT id FROM halos where aexp=1.0005 and M_hc > 1e+12"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

        #case: main_halos_only = True

        result = self.sim.get_halo_ids(main_halos_only = True)

        true_query = "SELECT id FROM halos where aexp=1.0005 and is_main_halo=1"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

        #case: min_halo_particles

        result = self.sim.get_halo_ids(min_halo_particles = 1e4)

        true_query = "SELECT id FROM halos where aexp=1.0005 and num_particles > 10000.0"
        mock_execute.assert_called_with(true_query)
        self.assertEqual(result, true_result)

    @mock.patch.object(reader.Simulation,'execute')
    def test_get_halo_epochs(self, mock_execute):
        mock_execute.return_value = [(1.0005,), (0.9015,), (0.8001,)]

        result = self.sim.get_halo_epochs()

        true_query = "SELECT DISTINCT aexp FROM halos ORDER BY aexp DESC"
        true_result = np.array([1.0005, 0.9015, 0.8001])

        mock_execute.assert_called_with(true_query)
        self.assertTrue((result == true_result).all())

    @mock.patch.object(reader.Simulation,'execute_df')
    def test_get_progenitor_ids(self, mock_execute):
        mock_execute.return_value = True

        self.sim.get_progenitor_ids([1,2,3])

        true_query = "SELECT id, aexp, z0_parent_id FROM halos"
        true_query += " inner join mergertree on halos.id=mergertree.child_id"
        true_query += " and halos.aexp=mergertree.child_aexp where"
        true_query += " is_main_line = 1 and z0_parent_id in (1, 2, 3)"
        true_query += " ORDER BY halos.aexp ASC"

        mock_execute.assert_called_with(true_query)


def assertFrameEqual( df1, df2 ):
    """ Assert that two dataframes are equal, ignoring ordering of columns"""

    return assert_frame_equal( df1.sort( axis=1) , df2.sort( axis=1) , check_names = True )


if __name__ == '__main__':
    conn_suite = unittest.TestLoader().loadTestsFromTestCase(ConnectionTest)
    reader_suite = unittest.TestLoader().loadTestsFromTestCase(ReaderTest)

    full_suite = unittest.TestSuite([conn_suite, reader_suite])
    unittest.TextTestRunner(verbosity=2).run(full_suite)

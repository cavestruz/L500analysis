Author: Camille Avestruz

Email: avestruz@uchicago.edu

Date: 2016-02-07
--------------

This is the repository for doing basic analysis with the Omega 500
dataset stored in the database.  It includes Kaylea's python wrapper
to query profiles and halo properties (in L500analysis/caps), and
basic data IO including the framework to derive any fields.  The
data_io package combines basic reading of database profiles and halo
properties with derived profiles and properties.  Derived field
calculations are done in the derived_fields package.  Any additional
code should be added to the appropriate subdirectory structure in
L500analysis/plotting, and L500analysis/derived_fields.

--------------
Python Package
--------------

1. Add the directory **containing** L500analysis to your python path.
   e.g. If L500analysis is in <path2L500>/L500analysis, you can use
   
   >>export PYTHONPATH="<path2L500>:$PYTHONPATH"

2. Dependencies : 

   (a) The analysis code expects you to have cosmolopy installed.  If
   you are using a linux machine, you can use:

   >> pip install cosmolopy

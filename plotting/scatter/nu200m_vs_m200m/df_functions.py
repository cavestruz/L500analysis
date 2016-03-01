from __future__ import division
import numpy as np
from data_io.derived_fields import *
from data_io.derived_field_functions import *
from constants import *

def _total_halo_mass(profiles, *args, **kwargs) :

    halo_id = kwargs['halo_id']

    return [ profiles['M_dark'],
             profiles['M_dark'],
             profiles['M_dark'] ]


add_derived_field('M_tot', function=_total_halo_mass,
                  combine_function=sum_profiles)


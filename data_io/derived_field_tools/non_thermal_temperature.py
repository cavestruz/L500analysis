import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *

def calculate_rms(average=None, sigma_std=None) :

    return np.sqrt(average**2+sigma_std**2)


def calculate_T_nonthermal(sigr=None, vr=None,
                           sigt=None, vt=None) :

    return (calculate_rms(vr,sigr)**2 + \
            calculate_rms(vt,sigt)**2) *\
            1e10 * constants.mu * constants.mp / 3

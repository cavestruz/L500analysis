import L500analysis.utils.constants as constants
from L500analysis.utils.utils import *

def calculate_rms(average=None, sigma_std=None) :
    '''Root mean square of a quantity'''
    return np.sqrt(average**2+sigma_std**2)


def calculate_T_nonthermal(sigr=None, vr=None,
                           sigt=None, vt=None) :
    '''Tnt in keV'''

    return ( calculate_rms(vr,sigr)**2 + calculate_rms(vt,sigt)**2 ) \
        * 1e10 * constants.mu * constants.mp * constants.erg2keV / 3

def calculate_Ttot(sigr=None, vr=None,
                   sigt=None, vt=None,
                   Tmw=None) :
    '''Ttot in keV'''
    Tnt_in_keV = calculate_T_nonthermal(sigr=sigr, vr=vr,
                                 sigt=sigt, vt=vt)

    Tmw_in_keV = Tmw * constants.kb * constants.erg2keV

    return Tnt_in_keV + Tmw_in_keV

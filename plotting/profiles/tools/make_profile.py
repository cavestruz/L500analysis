'''Set up a profile to be plotted, interpolating for log-log plots,
lin-log plots, etc.'''

from numpy import *
from L500analysis.utils.constants import rbins, linear_rbins

def make_profile(profile_rbins=rbins, x=None,y=None) :

    return 10**interp(profile_rbins, x, log10(y))

def make_profile_linear(profile_rbins=linear_rbins, x=None,y=None) :
    
    return interp(profile_rbins, x, y)

def calculate_dv(rin=None,rout=None,r=None) :
    '''Given radii in a sphere, calculates differential volume bins'''
    if rin != None and rout != None: 
        return 4.*pi*(rout-rin)**3./3.
    else : 
        return 4.*pi*concatenate((r[:1],diff(r)))**3./3.


class MakeProfile :
    def __init__(self, numbins=99, x=None, y=None, xlog=True, ylog=True) :
        self.num_bins = numbins
        self._create_volume_bins()

        # Radial bins, equally spaced in log space for scaled profiles
        # (for averaging)
        self.rbins = 10**arange(log10(0.01),log10(8.0),0.05)
        self.x = x
        self.y = y
        self._create_radial_data(xlog)
        self._create_profile_data(ylog)

    def _create_volume_bins(self) :
        rr = 10**linspace(log10(10),log10(1e4),num=self.num_bins)
        dlogr = log10(rr[1])-log10(rr[0])
        self.rmid = zeros(num_bins)
        self.dvol = zeros(num_bins)
        self.rmid[0] = 5.0
        self.dvol[0] =  4*pi/3.0*rr[0]**3.0
        for i in xrange(1,self.num_bins) :
            self.rmid[i] = 10**(1+dlogr*(i-0.5))
            self.dvol[i] = 4*pi/3.0*(rr[i]**3.0-rr[i-1]**3.0)        

    def _create_radial_data(self,xlog) :
        self.x_interpolated = self.rbins

    def _create_profile_data(self,ylog) :        
        self.y_interpolated = 10**interp(self.rbins, self.x, 
                                             log10(self.y))
        

# interp( rbins, rmid/h.rhalo,  log10(h.tpro*erg2keV/h.Thalo))

# 10**interp (0.0, log10(rmid/h.rhalo), log10(h.tottpro*erg2keV/h.Thalo))

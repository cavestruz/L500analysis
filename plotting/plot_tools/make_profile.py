from numpy import *

''' Set up a profile to be plotted '''

class MakeProfile :
    def __init__(self, numbins=99) :
        self.num_bins = numbins
        rr = 10**linspace(log10(10),log10(1e4),num=num_bins)
        drl = log10(rr[1])-log10(rr[0])
        self.rmid = zeros(num_bins)
        self.dvol = zeros(num_bins)
        self.rmid[0] = 5.0
        self.dvol[0] =  4*pi/3.0*rr[0]**3.0
        for i in xrange(1,num_bins) :
            self.rmid[i] = 10**(1+drl*(i-0.5))
            self.dvol[i] = 4*pi/3.0*(rr[i]**3.0-rr[i-1]**3.0)

        # Radial bins for scaled profiles (for averaging)                                                                
        self.rbins = 10**arange(log10(0.01),log10(8.0),0.05)
        

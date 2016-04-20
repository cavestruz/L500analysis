import numpy as np

gravc = 6.673e-8 #cm^3/g/s^2
mp = 1.6726e-24
mu = 0.59
mue = 1.14
Msun2g = 1.9891e33
g2Msun = 1./Msun2g
Mpc2cm = 3.08567758e24 
kpc2cm = Mpc2cm/1e3 
cm2kpc = 1./kpc2cm
km2m = 1e3
km2cm = 1e5
cm2km = 1/km2cm

keV2erg = 1.602177e-9
erg2keV = 1.0/keV2erg
kb = 1.38e-16 # Boltzmann Constant erg/K
K2keV = kb*erg2keV

omega_b = 0.0469
omega_m = 0.27
omega_l = 0.73
fb = omega_b/omega_m
fbc = omega_b/(omega_m-omega_b)
hubble = 0.7
H_0 = 100.0*1.0e5/Mpc2cm*hubble
#from h^2Msun/kpc^3 to g/cm^3                               

rhoc_0 = (3.0/(8.0*np.pi*gravc))*H_0*H_0 # g/cm^3 (?)
delta_c = 1.1686
power_spectrum_index_n = 0.96 # P(k) \propto k^n                                 
sigma_8 = 0.820


denconvert = hubble*hubble*Msun2g/(Mpc2cm/1000.0)**3


rbins = 10**np.arange(np.log10(0.01),np.log10(8.0),0.05)
linear_rbins = 10.**np.arange(-1.,4.,0.002)

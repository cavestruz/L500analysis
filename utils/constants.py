import numpy as np

gravc = 6.673e-8
mp = 1.6726e-24
mu = 0.59
mue = 1.14
Msun = 1.9891e33
Mpc = 3.08567758e24 #Mpc->cm     
kpc = Mpc/1e3 #kpc->cm

keV2erg = 1.602177e-9
erg2keV = 1.0/keV2erg
kb = 1.38e-16 # Boltzmann Constant erg/K

omega_b = 0.0469
omega_m = 0.27
omega_l = 0.73
fb = omega_b/omega_m
fbc = omega_b/(omega_m-omega_b)
hubble = 0.7
H_0 = 100.0*1.0e5/Mpc*hubble
#from h^2Msun/kpc^3 to g/cm^3                               

rhoc_0 = (3.0/(8.0*np.pi*gravc))*H_0*H_0 / Msun * (kpc**3.0) # h^2Msun/kpc^3
                                 
                    
denconvert = hubble*hubble*Msun/(Mpc/1000.0)**3

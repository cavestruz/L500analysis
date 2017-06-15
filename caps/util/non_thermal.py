#!/usr/bin/python

from pylab import *

from sg_filter import *
import sys
from numpy import array, pi, concatenate
from ..io import reader as db

def calc_prand(rmax, rho_gas, P_thermal, sig_rad, sig_tan):
    sigv2 = ( sig_rad**2 + sig_tan**2 ) / 3.
    Prand = rho_gas * sigv2*1e10
    return Prand

def calc_pturb(sim, aexp, id, clump_exclude=True ):
    G = 6.67428e-8

    num_bins = 99
    if clump_exclude:
        properties = ["rr","rho_gas","Ptherm", "Prand","sig_r", "sig_t", "v_t"]
    else:
        print "pturb values with clumps not excluded have not been imported into the database yet"
        die()

    profiles = sim.get_halo_profiles([id], ["Mtotal"], aexp, by_id=True)[id]
    pturb_profiles = sim.get_halo_profiles([id], properties, aexp, table="prand_profiles", by_id=True)[id]

    binr = pturb_profiles["rmid"]

    Mtrue = interp( binr, profiles["rmid"], profiles["Mtotal"] )

    # binrmid, binrr, Pth, Ptu, rhogas, cs, vr, sigr, vt, sigt, sigv, Ptuc, Pthc

    Pth = 10.**smooth( log10(pturb_profiles["Ptherm"]), 4, 2, 0 )[0:num_bins-1]
    dlogPth = smooth( log10(pturb_profiles["Ptherm"]), 4, 2, 1 )[0:num_bins-1]

    Pturb = 10.**smooth( log10(pturb_profiles["Prand"]), 4, 2, 0 )[0:num_bins-1]
    dlogPturb = smooth( log10(pturb_profiles["Prand"]), 4, 2, 1 )[0:num_bins-1]

    dlogrhosig2 = smooth( log10(1e10*pturb_profiles["rho_gas"]*pturb_profiles["sig_r"]**2), 4, 2, 1 )[0:num_bins-1]

    sigr = 1e5*smooth( pturb_profiles["sig_r"], 4, 2, 0)[0:num_bins-1]
    sigt = 1e5*smooth( pturb_profiles["sig_t"], 4, 2, 0)[0:num_bins-1]
    sigr2 = sigr*sigr
    sigt2 = sigt*sigt
    rhogas = 10**smooth( log10(pturb_profiles["rho_gas"]), 4, 2, 0 )[0:num_bins-1]
    vrot = 1e5*smooth(pturb_profiles["v_t"], 4, 2, 0)[0:num_bins-1]
    vrot2 = vrot*vrot

    dlogR = array([ log10(pturb_profiles["rmid"][bin+1]) - log10(pturb_profiles["rmid"][bin]) for bin in range(0,num_bins-1)])

    r = pturb_profiles["rmid"][0:num_bins-1] * 3.0856e21/0.7
    rr = pturb_profiles["rr"][0:num_bins-1] * 3.0856e21/0.7
    binr = pturb_profiles["rmid"][0:num_bins-1]

    Mhse = -r/(G*rhogas)*Pth*dlogPth/dlogR/(1.989e33/0.7)
    Mrand = -r/G*(sigr2*dlogrhosig2/dlogR + 2*sigr2 - sigt2)/(1.989e33/0.7)
    Mrot = r*vrot2/G/(1.989e33/0.7)

    Mtot = Mhse+Mrand+Mrot

    dPturb = dlogPturb/dlogR*Pturb/r
    dPth = dlogPth/dlogR*Pth/r

    Msigt2 = r*(sigt2)/G/(1.989e33/0.7)
    Msigr2 = -r*(2*sigr2)/G/(1.989e33/0.7)

    return ( binr, Mhse, Mrand, Mrot, Mtot, Mtrue, Pturb, Pth, dPturb, dPth, Msigt2, Msigr2 )

def calc_jeans(id, cluster_aexp, pturb_profiledir, dir, profiledir="profiles", clump_exclude=True ):
    G = 6.67428e-8 #cm3/g*s2
    cluster_aexp = str(cluster_aexp)

    num_bins = 99

    ( binr, Mhse, Mrand, Mrot, Mtot, Mtrue, Pturb, Pth, dPturb, dPth, Msigt2, Msigr2 ) = calc_pturb(id, cluster_aexp, pturb_profiledir, dir, profiledir, clump_exclude = clump_exclude)

    if clump_exclude:
    	pturb_vars = load_pturb_values(dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp+".dat",clusters=[id],num_bins=num_bins,aexpn=float(cluster_aexp))
    	( binrmid, binrr, dvr_term, dvtheta_term, dvphi_term, dsig2dr, dsig2dtheta, dsig2dphi, sigrtheta2)  = load_jeans_profile(dir+"/"+pturb_profiledir+"/h_bbturb_jeans_pro_a"+cluster_aexp+".dat",float(cluster_aexp),clusters=[id],num_bins=num_bins)
    else:
    	pturb_vars = load_pturb_values(dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp+".dat",clusters=[id],num_bins=num_bins,aexpn=float(cluster_aexp))
    	( binrmid, binrr, dvr_term, dvtheta_term, dvphi_term, dsig2dr, dsig2dtheta, dsig2dphi, sigrtheta2)  = load_jeans_profile(dir+"/"+pturb_profiledir+"/h_bturb_jeans_pro_a"+cluster_aexp+".dat",float(cluster_aexp),clusters=[id],num_bins=num_bins)

    #convert kpc/h to cm
    r = binrmid[id][0:num_bins-1]* 3.0856e21/0.7 
    #r = binrr[id][0:num_bins-1]* 3.0856e21/0.7 #convert kpc/h to cm

    vr = smooth( pturb_vars[6][id], 4, 2, 0 )
    dvr =array([ vr[bin+1] - vr[bin] for bin in range(0,num_bins-1)])
    dr = array([ (pturb_vars[0][id][bin+1]) - (pturb_vars[0][id][bin]) for bin in range(0,num_bins-1)])

    dvr = vr[0:num_bins-1]*dvr/dr/(3.0856e21/0.7)*1e5
    
    #dvr = smooth( dvr_term[id], 4, 2, 0)[0:num_bins-1]
    
    dvtheta = smooth( dvtheta_term[id], 4, 2, 0)[0:num_bins-1] 
    dvphi = smooth( dvphi_term[id], 4, 2, 0)[0:num_bins-1]

    ds2dr = smooth(dsig2dr[id], 4, 2, 0)[0:num_bins-1]
    ds2dthe = smooth(dsig2dtheta[id], 4, 2, 0)[0:num_bins-1]
    ds2dphi = smooth(dsig2dphi[id], 4, 2, 0)[0:num_bins-1]
    srthe2 =  smooth(sigrtheta2[id], 4, 2, 0)[0:num_bins-1]

    Mrand2 = -1*r*r/G*ds2dr*1e5/(1.989e33/0.7) + Msigr2 + Msigt2
    Mcrossing = (-1*r*r/G*(ds2dthe + ds2dphi)*1e5 - r/G*srthe2*1e10)/(1.989e33/0.7)
    Mstream = -1*r*r*(dvr + dvtheta + dvphi)/G/(1.989e33/0.7)*1e5 - Mcrossing - Mrand + Msigt2

    Mtot = Mhse + Mrand + Mstream + Mcrossing

    return ( binr, Mhse, Mrand, Mrot, Mstream, Mcrossing, Mtot, Msigt2 )

def calc_euler(id, cluster_aexp, pturb_profiledir, dir, profiledir="profiles", clump_exclude=True ):
    G = 6.67428e-8

    num_bins = 99
    cluster_aexp = str(cluster_aexp)
    #binrmid,binrr,rhogas,Pth, cs,vr,sigr,vtheta,sigtheta,vphi,sigphi
    if clump_exclude:
        pturb_vars = load_pturb_profile(dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins )
        euler_vars = load_euler_profile(dir+"/"+pturb_profiledir+"/h_bbturb_euler_pro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins)
    else:
    	pturb_vars = load_pturb_profile(dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins )
    	euler_vars = load_euler_profile(dir+"/"+pturb_profiledir+"/h_bturb_euler_pro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins)
    mpro_vars = load_cumulative_profile(dir+"/"+profiledir+"/h_bmpro_a"+cluster_aexp+".dat",clusters=[id],num_bins=num_bins)

    (dPth_term, dvr_term, dvtheta_term, dvphi_term, vt2) = euler_vars[2:7]
    (vr_term, vtheta_term, vphi_term, vrot2) = euler_vars[2:6]
   
    Pth = 10.**smooth( log10(pturb_vars[3][id]), 4, 2, 0 )[0:num_bins-1]
    dlogPth = smooth( log10(pturb_vars[3][id]), 4, 2, 1 )[0:num_bins-1]

    rhogas = 10**smooth( log10(pturb_vars[2][id]), 4, 2, 0 )[0:num_bins-1]
    dlogR = array([ log10(pturb_vars[0][id][bin+1]) - log10(pturb_vars[0][id][bin]) for bin in range(0,num_bins-1)])

    vrot2 = 1e10*smooth(vt2[id], 4, 2, 0)[0:num_bins-1]
    dPthdr = smooth (dPth_term[id], 4, 2, 0)[0:num_bins-1]
    
    r = euler_vars[0][id][0:num_bins-1] * 3.0856e21/0.7
    rr = euler_vars[1][id][0:num_bins-1] * 3.0856e21/0.7
    surface_area = 4.0*pi*r*r

    dvr = smooth( dvr_term[id], 4, 2, 0)[0:num_bins-1] 
    dvtheta = smooth( dvtheta_term[id], 4, 2, 0)[0:num_bins-1] 
    dvphi = smooth( dvphi_term[id], 4, 2, 0)[0:num_bins-1] 
    
    binr = pturb_vars[0][id][0:num_bins-1]
    Mtherm = -1./(4.*pi*G)*1/rhogas*Pth*dlogPth/dlogR/r/(1.989e33/0.7)*surface_area
    Mtherm2 = -1./(4.*pi*G)*(dPthdr)*1.e5/(1.989e33/0.7)
    Mrot = 1./(4.*pi*G)*(vrot2*1e10)/r/(1.989e33/0.7)
    Mstream = -1./(4.*pi*G)*(dvr + dvtheta + dvphi)*1e15/(1.989e33/0.7)

    Mtot = Mtherm+Mrot+Mstream
    Mtrue = interp( binr, mpro_vars[0][id], mpro_vars[3][id] )

    return ( binr, Mtherm, Mrot, Mstream, Mtot )

"""
calculate acceleration term from three neighboring epochs
aexp2 < aexp < aexp1
aexp = middle epoch
aexp1 = later epoch
aexp2 = earlier epoch
"""
def calc_accel(id, id1, id2, cluster_aexp, cluster_aexp1, cluster_aexp2, pturb_profiledir, dir, profiledir="profiles", clump_exclude=True):
    G = 6.67428e-8

    num_bins = 99
    cluster_aexp = str(cluster_aexp)
    cluster_aexp1 = str(cluster_aexp1)
    cluster_aexp2 = str(cluster_aexp2)

    if clump_exclude:
        pturb_vars = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins)
        pturb_vars1 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp1+".dat", float(cluster_aexp1), clusters=[id1],num_bins=num_bins)
        pturb_vars2 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp2+".dat", float(cluster_aexp2), clusters=[id2],num_bins=num_bins)
    else:
     	pturb_vars = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins)
    	pturb_vars1 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp1+".dat", float(cluster_aexp1), clusters=[id1],num_bins=num_bins)
    	pturb_vars2 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp2+".dat", float(cluster_aexp2), clusters=[id2],num_bins=num_bins)
    
    vr = smooth(pturb_vars[6][id], 4, 2, 0)
    vr1 = smooth(pturb_vars1[6][id1], 4, 2, 0)
    vr2 = smooth(pturb_vars2[6][id2], 4, 2, 0)

    binr = pturb_vars[0][id]

    if (float(cluster_aexp) > 1):
        z = 0.
    else:
        z = 1./float(cluster_aexp)-1
        
    if (float(cluster_aexp1) > 1):
        z1 = 0.
    else:
        z1 = 1./float(cluster_aexp1)-1
        
    if (float(cluster_aexp2) > 1):
        z2 = 0.
    else:
        z2 = 1./float(cluster_aexp2)-1

    t  = cosmocalc(1./float(cluster_aexp)-1, WM=0.3,WV=0.7)["zage_Gyr"]
    t1 = cosmocalc(1./float(cluster_aexp1)-1, WM=0.3,WV=0.7)["zage_Gyr"]
    t2 = cosmocalc(1./float(cluster_aexp2)-1, WM=0.3,WV=0.7)["zage_Gyr"]

    r = pturb_vars[0][id]* 3.0856e21/0.7
    
    dvr1 = (vr1 - vr)
    dvr2 = (vr - vr2)

    dt1 = (t1 - t)
    dt2 = (t - t2)

   # print t1-t2
    
   # dvrdt = (vr1-vr2)/(t1-t2)
    dvrdt = (dvr1/dt1)*(dt1)/(dt1+dt2)+(dvr2/dt2)*(dt2)/(dt1+dt2)
    Maccel = -r*r*dvrdt/G/(1.989e33/0.7)*(1e5)/(1e9*3.15569e7)
    Maccel = Maccel[0:num_bins-1]
    binr = binr[0:num_bins-1]

    return ( binr, Maccel)

def calc_dvrdt(id, id1, id2, cluster_aexp, cluster_aexp1, cluster_aexp2, pturb_profiledir, dir, profiledir="profiles", clump_exclude=True):
    G = 6.67428e-8

    num_bins = 99
    if clump_exclude:
        pturb_vars = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins)
        pturb_vars1 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp1+".dat", float(cluster_aexp1), clusters=[id1],num_bins=num_bins)
        pturb_vars2 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bbturbpro_a"+cluster_aexp2+".dat", float(cluster_aexp2), clusters=[id2],num_bins=num_bins)
    else:
        pturb_vars = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp+".dat", float(cluster_aexp), clusters=[id],num_bins=num_bins)
        pturb_vars1 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp1+".dat", float(cluster_aexp1), clusters=[id1],num_bins=num_bins)
        pturb_vars2 = load_pturb_values( dir+"/"+pturb_profiledir+"/h_bturbpro_a"+cluster_aexp2+".dat", float(cluster_aexp2), clusters=[id2],num_bins=num_bins)


    vr = pturb_vars[6][id]
    vr1 = pturb_vars1[6][id1]
    vr2 = pturb_vars2[6][id2]

    binr = pturb_vars[0][id]

    if (float(cluster_aexp) > 1):
        z = 0.
    else:
        z = 1./float(cluster_aexp)-1
        
    if (float(cluster_aexp1) > 1):
        z1 = 0.
    else:
        z1 = 1./float(cluster_aexp1)-1
        
    if (float(cluster_aexp2) > 1):
        z2 = 0.
    else:
        z2 = 1./float(cluster_aexp2)-1

    t  = cosmocalc(1./float(cluster_aexp)-1, WM=0.3,WV=0.7)["zage_Gyr"]
    t1 = cosmocalc(1./float(cluster_aexp1)-1, WM=0.3,WV=0.7)["zage_Gyr"]
    t2 = cosmocalc(1./float(cluster_aexp2)-1, WM=0.3,WV=0.7)["zage_Gyr"]

    r = pturb_vars[0][id]* 3.0856e21/0.7
    
    dvr1 = (vr1 - vr)
    dvr2 = (vr - vr2)

    dt1 = (t1 - t)
    dt2 = (t - t2)

    print t1-t2
    
    dvrdt = (vr1-vr2)/(t1-t2)/(1e9*3.15569e7)
    
    return ( binr, dvrdt)


#!/usr/bin/python

from numpy import zeros, median, array
from scipy import stats
from scipy.optimize import leastsq

def compute_mean_variance( cluster_profiles, clusters=None, dict=True ):
        if dict == True:
            bins = len(cluster_profiles[cluster_profiles.keys()[0]])
        else:
            bins = len(cluster_profiles[0])

        mean_val = zeros(bins)
        sig_up = zeros(bins)
        sig_down = zeros(bins)
        num_up = zeros(bins)
        num_down = zeros(bins)

        if dict == True:
            if clusters is None:
                    ids = cluster_profiles.keys()
            else:
                    ids = clusters

            for id in ids:
                    mean_val += cluster_profiles[id]

            mean_val /= float(len(ids))

        else:
            for profile in cluster_profiles:
                mean_val += profile

            mean_val /= float(len(cluster_profiles))



        if dict == True:

            for id in ids:
                for i,val in enumerate(cluster_profiles[id]):
                    if ( val > mean_val[i] ):
                        sig_up[i] += (val-mean_val[i])**2
                        num_up[i] += 1
                    else:
                        sig_down[i] += (val-mean_val[i])**2
                        num_down[i] += 1

        else:
            for profile in cluster_profiles:
                for i,val in enumerate(profile):
                    if ( val > mean_val[i] ):
                        sig_up[i] += (val-mean_val[i])**2
                        num_up[i] += 1
                    else:
                        sig_down[i] += (val-mean_val[i])**2
                        num_down[i] += 1
        sig_up /= num_up
        sig_down /= num_down

        return (mean_val,sig_up,sig_down)


def compute_median_quartiles ( cluster_profiles, clusters=None, dict=True ):

    if dict == True:
        bins = len(cluster_profiles[cluster_profiles.keys()[0]])
    else:
        bins = len(cluster_profiles[0])

    median_val = zeros(bins)
    upq = zeros(bins)
    lowq = zeros(bins)

    if dict == True:
        a = array(cluster_profiles.values())
        median_val = median(a, axis = 0)
        aT = array(cluster_profiles.values()).T
    else:
        median_val = median(cluster_profiles, axis=0)
        aT = array(cluster_profiles).T

    for i in range(bins):
        upq[i] = stats.scoreatpercentile(aT[i],75)
        lowq[i] = stats.scoreatpercentile(aT[i],25)

    return (median_val, upq, lowq)

def powerlaw(p, y, x):
        A,alpha = p
        err = y - A-alpha*(x)
        return err

def fit_powerlaw(x, y, xstart, ystart):
        plsq1 = leastsq( powerlaw, (xstart,ystart), args=(log10(y),log10(x)),full_output=1 )
        covar1 = plsq1[1]
        A1 = 10.**plsq1[0][0]
        alpha1 = plsq1[0][1]
        alpha1err = sqrt(covar1[0][0])
        A1err = sqrt(covar1[1][1])*A1

        return A1, A1err, alpha1, alpha1err





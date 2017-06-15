from math import *
from numpy import *


def resub(D, rhs):

    """ solves D D^T = rhs by resubstituion.
        D is lower triangle-matrix from cholesky-decomposition """

    M = D.shape[0]
    x1= zeros((M,),float)
    x2= zeros((M,),float)

    # resub step 1
    for l in range(M): 
        sum = rhs[l]
        for n in range(l):
            sum -= D[l,n]*x1[n]
        x1[l] = sum/D[l,l]

    # resub step 2
    for l in range(M-1,-1,-1): 
        sum = x1[l]
        for n in range(l+1,M):
            sum -= D[n,l]*x2[n]
        x2[l] = sum/D[l,l]

    return x2
   

def calc_coeff(num_points, pol_degree, diff_order=0):

    """ calculates filter coefficients for symmetric savitzky-golay filter.
        see: http://www.nrbook.com/a/bookcpdf/c14-8.pdf

        num_points   means that 2*num_points+1 values contribute to the
                     smoother.

        pol_degree   is degree of fitting polynomial

        diff_order   is degree of implicit differentiation.
                     0 means that filter results in smoothing of function
                     1 means that filter results in smoothing the first 
                                                 derivative of function.
                     and so on ...

    """

    # setup normal matrix
    A = zeros((2*num_points+1, pol_degree+1), float)
    for i in range(2*num_points+1):
        for j in range(pol_degree+1):
            A[i,j] = pow(i-num_points, j)
        
    # calculate diff_order-th row of inv(A^T A)
    ATA = dot(A.transpose(), A)
    rhs = zeros((pol_degree+1,), float)
    rhs[diff_order] = 1
    D = linalg.cholesky(ATA)
    wvec = resub(D, rhs)

    # calculate filter-coefficients
    coeff = zeros((2*num_points+1,), float)
    for n in range(-num_points, num_points+1):
        x = 0.0
        for m in range(pol_degree+1):
            x += wvec[m]*pow(n, m)
        coeff[n+num_points] = x
    return coeff

def savgol(np,nl,nr,ld,m):
	index = zeros(m)
	A = zeros(m,m)
	b = zeros(m)

	for ipj in arange(2*m):
		if ipj == 0:
			s = 0.0
		else:
			s = 1.0

		s += sum([k**ipj for k in arange(nr)])	
		s += sum([-k**ipj for k in arange(nl)]) 
		mm = min(ipj,2.*m-ipj)
		for imj in arange(-mm,mm,2.0):
			a[(ipj+imj)/2,(ipj-imj)/2] = s
		
        #ludcmp(a,m+1,indx,&d);
        #b[ld+1]=1.0
        #lubksb(a,m+1,indx,b);

	coeff = zeros(np)

	for k in xrange(-nl,nr+1):
		s = b[0]
		for mm in xrange(m):
			s += b[mm+1]*pow(float(k),float(mm))
		kk = (np-k)%np
		coeff[kk] = s

	return coeff

#def smooth(signal, coeff):
#    
#    """ applies coefficients calculated by calc_coeff()
#        to signal """
#    
#    N = size(coeff-1)/2
#    res = convolve(signal, coeff)
#    return res[N:-N]

def smooth(signal,mbin,m,diff_order=0):
	smoothed = zeros(len(signal))
	for i in xrange(len(signal)):
		nl = nr = mbin

		if ( i < mbin ):
			nl = i
			nr = i
		elif ( i > len(signal)-mbin-1 ):
			nr = len(signal)-i-1
			nl = nr

		nc = nl+nr+1
		if ( nc > 1 ):
			coeff = calc_coeff(nl, m, diff_order)
		#	print coeff, sum(coeff)
		#for k in xrange(-nl,nr):
		#	print k, nl, nr, nc, signal[i+k], (nc-k)%nc, coeff[(nc-k)%nc]
			smoothed[i] = sum([signal[i+k]*coeff[k+nl] for k in xrange(-nl,nr+1)])
		else:
			if ( diff_order == 0 ):
				smoothed[i] = signal[i]		
			else:
				smoothed[i] = 0.0
      	return smoothed

#y = array([x**2 for x in arange(0,10,0.1)])
#yd = array([2*x for x in arange(0,10,0.1)])
#y1 = smooth(y,4,2,0)
#y2 = smooth(y,4,2,1)/0.1
#print ((y2-yd)/yd)


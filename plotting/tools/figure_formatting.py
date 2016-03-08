from matplotlib.ticker import AutoMinorLocator
from matplotlib import rc
rc('legend',fontsize=8)


class MyLogFormatter(matplotlib.ticker.LogFormatter) :
    def __call__(self,x,pos=None) :
        if (log10(x)) < 3 and (log10(x)) > -3 :
            return "$%g$" % (x,)
        else :
            return "$10^{%g}$" % (log10(x),)

main_fig = [0.15, 0.15, 0.80, 0.80]
sub_fig = [0.15, 0.15, 0.0, 0.0]

llimstr = "2.9e14"
ulimstr = "2e15"

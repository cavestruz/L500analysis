import matplotlib
from numpy import log10
from matplotlib.pyplot import *
from matplotlib.ticker import AutoMinorLocator
from collections import OrderedDict

class MyLogFormatter(matplotlib.ticker.LogFormatter) :
    def __call__(self,x,pos=None) :
        if (log10(x)) < 3 and (log10(x)) > -3 :
            return "$%g$" % (x,)
        else :
            return "$10^{%g}$" % (log10(x),)

class PlotAxes :
    def __init__(self, figdir='./figures/',
                 figname=None,figformat='.pdf',
                 figsize=(5,5), 
                 axes=[[0.15,0.15,0.8,0.8]],
                 axes_labels=None,
                 use_axes_labels=True,
                 xlabel=None, 
                 xlog=False, ylog=False,
                 xlim=None,
                 ylims=None
                 ) :
        self.figdir=figdir
        self.figname=figname
        self.figformat=figformat
        self.figure = figure(figsize=figsize)
        self.axes = [self.figure.add_axes(axis) for axis in axes]

        if axes_labels == None : axes_labels = range(len(axes))
        self.axes = OrderedDict(zip(axes_labels,self.axes))

        self._legend = {}
        self.xlog,self.ylog=xlog,ylog
        # Do figure formatting
        self._setxlim(xlim)
        self._setylims(ylims)
        self._setxlabel(xlabel)
        if use_axes_labels : 
            self._setylabel(axes_labels)

        self._setlogformat(self.xlog,self.ylog)

    def _setylabel(self, axes_labels) :

        for axis,label in zip(self.axes.values(),axes_labels) :
            axis.set_ylabel(label,fontsize='xx-large')

        

    def savefig(self) :
        print("Saving in "+self.figdir+self.figname+self.figformat)
        self.figure.savefig(self.figdir+self.figname+self.figformat)
                 
    def _setxlim(self,xlim) :
        if xlim == None : return

        for axis in self.axes.values() :
            axis.set_xlim(xlim)

    def _setylims(self,ylims) :
        if ylims == None : return

        for axis,ylim in zip(self.axes.values(),ylims) :
            axis.set_ylim(ylim)

    def _setxlabel(self,xlabel) :

        for axis in self.axes.values()[:-1] :
            axis.get_xaxis().set_ticklabels([])
        if xlabel == None : return
        self.axes.values()[-1].set_xlabel(xlabel,fontsize='xx-large')        
        
    def _setlogformat(self,xlog,ylog) :
        if xlog : 
            for axis in self.axes.values() :
                self._make_xlogscale(axis)
        if ylog :
            for axis,yl in zip(self.axes.values(),ylog) :
                if yl : self._make_ylogscale(axis)
                    
    def _make_ylogscale(self,axis) :
        axis.set_yscale('log')
        axis.yaxis.set_major_formatter(MyLogFormatter())

    def _make_xlogscale(self,axis) :
        axis.set_xscale('log')
        axis.xaxis.set_major_formatter(MyLogFormatter())
        

    def set_legend(self,axes_label=0, **kwargs) :
        
        self._legend[axes_label] = self.axes[axes_label].legend(**kwargs)

    def color_legend_texts(self,axes_label=None,no_line=True):
        """Color legend texts based on color of corresponding lines"""

        legend=self._legend[axes_label]
        for line, txt in zip(legend.get_lines(), legend.get_texts()):
            txt.set_color(line.get_color())  
        if no_line : legend.handlelength = 0
            
            

llimstr = "2.9e14"
ulimstr = "2e15"

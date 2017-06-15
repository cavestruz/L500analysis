#!/usr/bin/env python

import struct
import sys
import os
import re

import numpy as np
from pylab import plt

from matplotlib.colors import LogNorm

def read_visualization_data(vis_file, selection = None):
    """
    reads in .dat files output by the visualization code.
    vis_file: file for to be read in
    selection: pixel size of map to be output
    returns image, size of the pixel in Mpc/h, and pixel values in Mpc/h
    """

    data = open(vis_file, "rb").read()
    
    fmt = "<i6d"
    headersize = struct.calcsize(fmt)
    header = struct.unpack(fmt, data[0:headersize])

    num_pixels = header[0]
 #   Lbox = header[1]
 #   center = header[2:5]
    width = header[5]
#    depth = header[6]
    
    fmt = str(num_pixels*num_pixels)+"d"
    image = struct.unpack(fmt, data[headersize:])

    image2d = np.reshape(image, (num_pixels, num_pixels))

    if selection is not None :
        image2d = image2d[num_pixels/2-selection[0]/2:num_pixels/2+selection[0]/2,
                          num_pixels/2-selection[1]/2:num_pixels/2+selection[1]/2]
    else :
        selection = [num_pixels, num_pixels]

    pixelsize = width/num_pixels * 1000.0 #kpc/h

    pixel_values = np.arange(-selection[0]/2, selection[1]/2)*pixelsize/1000.

    return image2d, pixelsize, pixel_values


def convert_all_to_png(vis_path, out_dir = "maps_png", size = None) :

    units = { 'gas_density' : 'Gas Density [g/cm$^3$]',
              'Tm' : 'Temperature [K]',
              'Tew' : 'Temperature [K]',
              'S' : 'Entropy []',
              'dm' : 'DM Density [g/cm$^3$]',
              'v' : 'Velocity [km/s]' }

    log_list = ['gas_density']

    for vis_file in os.listdir(vis_path) :
        if ".dat" not in vis_file :
            continue
        print "converting %s" % vis_file
        map_type = re.search('sigma_(.*)_[xyz]', vis_file).group(1)

        (image, pixel_size, axis_values) = read_visualization_data(vis_path+"/"+vis_file, size)
        print "image width in Mpc/h: ", axis_values[-1]*2.0

        x, y = np.meshgrid( axis_values, axis_values )

        cmap_max = image.max()
        cmap_min = image.min()


        ''' plotting '''
        plt.figure(figsize=(5,4))

        if map_type in log_list:
            plt.pcolor(x,y,image, norm=LogNorm(vmax=cmap_max, vmin=cmap_min))
        else :
            plt.pcolor(x,y,image, vmax=cmap_max, vmin=cmap_min)

        cbar = plt.colorbar()
        if map_type in units.keys() :
            cbar.ax.set_ylabel(units[map_type])

        plt.axis([axis_values[0], axis_values[-1],axis_values[0], axis_values[-1]])

        del image

        plt.xlabel(r"$Mpc/h$", fontsize=18)
        plt.ylabel(r"$Mpc/h$", fontsize=18)

        out_file = vis_file.replace("dat", "png")

        plt.savefig(out_dir+"/"+out_file, dpi=150 )

        plt.close()
        plt.clf()



def define_velocity_projection(proj):

    if proj == "x":
        plot_x = "z"; plot_y = "y"
    elif proj == "y":
        plot_x = "z"; plot_y = "x"
    elif proj == "z":
        plot_x = "x"; plot_y = "y"
    else:
        print "Unknown projection. Choose from 'x', 'y', or 'z'"
        sys.exit(1)

    return plot_x, plot_y


#!/usr/bin/python

import re
import numpy as np
import pandas as pd


def read_halo_catalog(directory, filename) :

    filename = directory+"/"+filename
    halo_catalog = pd.read_table(filename, sep=r"\s+")

    clean_column_names(halo_catalog)

    return halo_catalog

def read_halo_catalog_numpy(directory, filename) :

    filename = directory+"/"+filename
    halo_catalog = np.genfromtxt(filename, names=True)

    new_names = []
    for i, name in enumerate(halo_catalog.dtype.names) :
        new_names.append(name.replace(str(i+1), ""))
        
    halo_catalog.dtype.names = new_names

    return halo_catalog

def read_profiles(directory, filename, columns=[]) :

    filename = directory+"/"+filename
    if len(columns) == 0 :
        profiles = pd.read_table(filename, sep=r"\s+")
        clean_column_names(profiles)
    else :
        profiles = pd.read_table(filename, sep=r"\s+", 
                                skip=1, columns=columns)

    profiles = profiles[profiles.r > 0]

    profiles["id"] = np.where(profiles.r < profiles.r.shift(), 1, 0).cumsum()

    return profiles


def clean_column_names(data):

    rename = {}

    regex = re.compile("(\(\d*\))")

    for column in data.columns.tolist() :
        new_name = column.replace("#", "")
        new_name = regex.sub("", new_name)

        rename[column] = new_name

    data.rename(columns=rename, inplace=True)





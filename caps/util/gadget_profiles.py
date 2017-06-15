import numpy as np
from math import pi, sqrt

mass_weighted_properties = ["T"]
volume_weighted_properties = ["RHO "]
extra_quantities = ["T_sl"]

def generate_profiles(raw_data, bins, halo_center) :

    singletons = ["r_in", "r_out", "Volume", "MASS"]
    quantities = raw_data.keys()+extra_quantities+singletons
    bin_values = dict(( q, [] ) for q in quantities)

    raw_data["POS "] = raw_data["POS "] - halo_center

    for i, bin in enumerate(bins[1:]) :
	print i

        in_bin = bins[i-1]
        out_bin = bin

        bin_data = select_bin(raw_data, in_bin, out_bin)

        #populate bins for weighting parameters
        bin_values["r_in"].append( in_bin )
        bin_values["r_out"].append( out_bin)
        bin_values["Volume"].append( 4./3.*pi*(out_bin**3 - in_bin**3) )
        bin_values["MASS"].append( np.sum(bin_data["MASS"]) )

        for q in quantities :

            if q in mass_weighted_properties :
                bin_values[q].append(np.sum(bin_data[q]*bin_data["MASS"])/bin_values["MASS"][-1])

            elif q in volume_weighted_properties :
                bin_values[q].append(np.sum(bin_data[q])/bin_values["Volume"][-1])

            elif q == "T_sl" :

                #calculate spectroscopic temperature
                mask = (bin_data["T"] > 1e6)
                T_cut_T = bin_data["T"][mask]
                T_cut_Rho = bin_data["RHO "][mask]
                T_cut = np.array(T_cut_T, T_cut_Rho).T

                numerator = np.sum(np.apply(calc_spec_temperature, T_cut, 0.25))
                denominator = np.sum(np.apply(calc_spec_temperature, T_cut, -0.75))
                bin_values["T_sl"].append( numerator/denominator )

            else :
                continue


    for q in quantities :
        bin_values[q] = np.array(bin_values[q]) 

    return bin_values


def calc_spec_temperature(data, exponent) :

    temperature = data[0]
    rho = data[1]

    return rho**2 * temperature**exponent



def calc_radius(pos) :

    return sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)

def select_bin(raw_data, in_bin, out_bin):

#    particle_radius = np.apply_along_axis(calc_radius, 1, raw_data["POS "])

    pos = raw_data["POS "].T
    mask = ((pos[0]**2+pos[1]**2+pos[2]**2) > in_bin) & ((pos[0]**2+pos[1]**2+pos[2]**2) < out_bin)

    bin  = {}
    for q in raw_data.keys() :
        if q == "HEAD" :
            continue

	bin[q] = np.ma.masked_where(np.ma.getmask(mask), raw_data[q])

    return bin    


import re
import os

import numpy as np
from astropy import units as u
from astropy.constants import G, c

M_gadget = 1.989e43 * u.g
L_gadget = 3.085678e21 * u.cm
v_gadget = 1e5 * u.cm / u.s
T_gadget = L_gadget / v_gadget
G_gadget = 43018.7

fact_GU_to_Gyr = 0.97779235

def get_snapshots(folder):

    def extract_number(file_path):
        match = re.search(r'snapshot_(\d+)\.hdf5', file_path)
        if match:
            return int(match.group(1))
        return 0  

    files = os.listdir(folder)
    hdf5_paths = [folder + f for f in files if f.endswith('.hdf5')]
    hdf5_paths = [path for path in hdf5_paths if 'bak' not in path]
    hdf5_paths = [path for path in hdf5_paths if 'snapshot' in path]
    hdf5_paths.sort(key=extract_number)

    return hdf5_paths

def get_fof_tab(folder):

    def extract_number(file_path):
        match = re.search(r'fof_subhalo_tab_(\d+)\.hdf5', file_path)
        if match:
            return int(match.group(1))
        return 0  

    files = os.listdir(folder)
    hdf5_paths = [folder + f for f in files if f.endswith('.hdf5')]
    hdf5_paths = [path for path in hdf5_paths if 'fof_subhalo_tab' in path]
    # hdf5_paths = [path for path in hdf5_paths if 'snapshot' in path]
    hdf5_paths.sort(key=extract_number)

    return hdf5_paths


def compute_cm(positions, lim=None, origin=None):

    if origin is None:
        origin = np.array([0,0,0])

    positions = np.array(positions) - origin
    
    r = np.linalg.norm(positions, axis=1)

    if lim is not None:
        #r = r[r<lim]
        positions = positions[r<lim]


    cm = np.mean(positions, axis=0)

    return cm + origin

def compute_recursive_cm(positions, lims):

    cm = np.array([0,0,0])
    for i, lim in enumerate(lims):
        cm = compute_cm(positions, lim, 
                        origin=cm
                        )
    return cm


def NFW_density_profile(r, rho_s, r_s):

    x = r/r_s
    return rho_s / (x * (1 + x)**2)


def NFW_mass_profile(r, rho_s, r_s):
    
    x = r/r_s
    return 4*np.pi*rho_s*r_s**3 * (np.log(1+x) - x/(1+x))

def NFW_density_profile_log(r, rho_s, r_s):

    x = r/r_s
    return np.log(rho_s / (x * (1 + x)**2))

def CDM_halo(r, rho_s, r_s, alpha, beta, gamma):

    """
    :rho_s: characteristic density
    :r_s: characteristic radius
    :alpha: Sharpness of transition (1)
    :beta: Slope of the outer profile (3)
    :gamma: Slope of the inner profile (1)
    """

    x = r/r_s
    num = rho_s
    den1 = x**gamma
    den2 = (1+x**alpha)**((beta-gamma)/alpha)

    return num/(den1*den2)  


def schechter_mf(M, phi_star, M_star, alpha):
    # M_star is the knee of the Schechter function
    return phi_star * (M/M_star)**(alpha) * np.exp(-M/M_star)


def format_scientific(num, prec=2):
    # Format the number in scientific notation with 2 decimal places for 'a'
    formatted =f"{num:.{prec}e}"

    # Split the string into the coefficient and exponent parts
    coefficient, exponent = formatted.split('e')
    # Remove the plus sign from the exponent if it exists
    exponent = exponent.replace('+', '')

    # Return the formatted string
    return rf"${coefficient} \times 10^{{{int(exponent)}}}$"
"""File for input/ouptput of FFA parameters.
Parameters are stored in a json file, and read in/out as a dict.

These parameters are:

##ANGLES:
theta_c  : Total angle covered by a cell
theta_ld : Angle covered by the long drift between cells
theta_d  : Angle covered by a D magnet
theta_sd : Angle covered by the short drift between D and F magnets
theta_f  : Angle covered by an F magnet

##FIELD PARAMETERS:
(Note that in the original lattice, the F and D parameters all had the same magnitude, with appropriate sign.)
B0_d     : Reference field of the D magnet
B0_f     : Reference field of the F magnet
k_d      : Field index of the D magnet
k_f      : Field index of the F magnet
r0       : Reference radius of the magnets  # TODO: What about offsets??

##MISC:
N_cell   : Total number of cells for modelling
name     : Name to give the lattice in tests etc.
r_min    : Minimum orbit radius (for display)
r_max    : Maximum orbit radius (for display)

All angles are stored in degrees, distances in cm, magnetic fields in T
"""
import json

def get_default_params():
    """A simple script to get the (approx) params used in the actual FFA, without worrying about file io."""
    param_dict = dict(theta_c=30.0,
                      theta_ld=4.75,
                      theta_d=3.43,
                      theta_sd=1.7,
                      theta_f=10.24,

                      B0_d=-1.6,
                      B0_f=1.6,
                      r0=540,
                      k_d=7.7,
                      k_f=7.7,

                      N_cell=1,
                      name="Default KURRI Cell",
                      r_min=485.4,
                      r_max=540)
    return param_dict

def get_fieldmap_dir():
    """Utility function to read the fieldmap directory from the settings file.
    Likely not a permanent function, better in future to return a cached property"""
    with open("settings.json") as settings:
        data = json.load(settings)
        fieldmap_dir = data["fieldmapDir"]
        return fieldmap_dir
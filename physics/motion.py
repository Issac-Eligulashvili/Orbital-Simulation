import numpy as np
from data.constants import mu
import math


def acceleration(r_vec):
    # Get radius magnitude
    r_mag = np.linalg.norm(r_vec)
    # get acceleration magnitude
    a_mag = (mu) / r_mag**2
    # return acceleration with mag and direction using unit vector
    return -a_mag * r_vec / r_mag

import numpy as np
from data.constants import planetary_mass, gravitational_constant
import math


def acceleration(r_vec):
    # Get radius magnitude
    r_mag = np.linalg.norm(r_vec)
    # get acceleration magnitude
    a_mag = (gravitational_constant * planetary_mass) / r_mag**2
    # return acceleration with mag and direction using unit vector
    return -a_mag * r_vec / r_mag


def velocity(r_vec):
    # Get acceleration and radius magnitudes
    a_mag = np.linalg.norm(acceleration(r_vec))
    r_mag = np.linalg.norm(r_vec)
    # Get velocity magnitude
    v_mag = math.sqrt(a_mag * r_mag)
    # Get perpendicular radius vector
    perpendicular_vec = np.array([-r_vec[1], r_vec[0]])
    # return velocity
    return v_mag * perpendicular_vec / r_mag

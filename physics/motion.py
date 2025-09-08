import numpy as np


def acceleration(r_vec, mu):
    # Get radius magnitude
    r_mag = np.linalg.norm(r_vec)
    # get acceleration magnitude
    a_mag = mu / r_mag**2
    # return acceleration with mag and direction using unit vector
    return -a_mag * r_vec / r_mag

def calculate_movement(r_vec, v_vec, dt, id, planets):
    acceleration_vectors = []
    for planet in planets:
        if planet.id == id:
            continue
        else:
            r = np.subtract(planet.position, r_vec)
            acceleration_vectors.append(acceleration(r, planet.mu))

    a = np.add.reduce(acceleration_vectors)


    r_new = (
            r_vec + v_vec * dt + 0.5 * a * dt ** 2
    )  # update the new position with the guess from the old acceleration
    acceleration_vectors = []
    for planet in planets:
        if planet.id == id:
            continue
        else:
            r = np.subtract(planet.position, r_new)
            acceleration_vectors.append(acceleration(r, planet.mu))

    a_new = np.add.reduce(acceleration_vectors) # get new acceleration with the new guessed position
    v_new = v_vec + 0.5 * (a + a_new) * dt  # calculate new velocity
    return r_new, v_new
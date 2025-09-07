import numpy as np
from vpython import sphere, vec, rate, color, scene, textures, box, cylinder, compound
from physics.motion import acceleration
from data.constants import v0

SCALE = 1e6  # 1 unit = 1,000 km

def animate_orbit_3d(r0, T, dt):
    ball = sphere(
    pos=vec(*r0) / SCALE, radius=0.1, color=color.yellow, make_trail=True
    )
    earth = sphere(pos=vec(0, 0, 0), radius=6378e3 / SCALE, texture=textures.earth)

    # Set background color and center of view
    scene.background = color.black
    scene.width = 800
    scene.height = 600
    r = np.array(r0)
    v = np.array([0, 0, v0])
    print(r, v)
    for _ in range(int(T / dt)):
        rate(60)

        a = acceleration(r)  # old acceleration
        r_new = (
            r + v * dt + 0.5 * a * dt**2
        )  # update the new position with the guess from the old acceleration
        a_new = acceleration(
            r_new
        )  # get new acceleration with the new guessed position
        v_new = v + 0.5 * (a + a_new) * dt  # calculate new velocity
        # Update the radius and velocity variables
        r = r_new
        v = v_new
        # change the satellite position
        ball.pos = vec(*r_new) / SCALE

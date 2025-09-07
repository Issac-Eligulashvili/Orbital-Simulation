import numpy as np
from fontTools.subset import retain_empty_scripts
from vpython import sphere, vec, rate, color, scene, textures, checkbox
from physics.motion import acceleration
from data.constants import v0

SCALE = 1e6  # 1 unit = 1,000 km

follow_satellite = False

def toggle_follow_satellite(evt):
    global follow_satellite
    if evt.checked:
        follow_satellite = True
    else :
        follow_satellite = False
    print(follow_satellite)

checkbox(bind=toggle_follow_satellite, text="Follow Satellite", checked=False)

def animate_orbit_3d(r0, T, dt):
    ball = sphere(
    pos=vec(*r0) / SCALE, radius=0.1, color=color.white, make_trail=True, trail_radius=0.02, retain=50)
    earth = sphere(pos=vec(0, 0, 0), radius=6378e3 / SCALE, texture=textures.earth)
    # Set background color and center of view
    scene.background = color.black
    scene.fullscreen = True
    r = np.array(r0)
    v = np.array([0, 0, v0])
    while True:
        rate(60)

        if follow_satellite:
            scene.follow(ball)
        else:
            scene.follow(None)
            scene.center = earth.pos

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

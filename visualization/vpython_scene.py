import numpy as np
from fontTools.subset import retain_empty_scripts
from vpython import sphere, vec, rate, color, scene, textures, checkbox, wtext, slider
from physics.motion import acceleration
from data.constants import v0, i
import datetime

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

i = np.radians(i)

#Get the amount of simulated time passed in seconds
time_sim = 0.0

rotation_x_matrix = np.array([[1,0,0],[0,np.cos(i), -np.sin(i)], [0,np.sin(i), np.cos(i)]])
wtext(text="\n\n")
time_display = wtext(text="Elapsed time: 0s")
wtext(text="\n\n")
dt_scalar = 1
min_value = 0.25
max_value = 10
def scale(evt):
    global dt_scalar
    dt_scalar = min_value + (max_value - min_value) * evt.value
    dt_slider_text.text = "{:1.2f}".format(dt_scalar)

dt_scalar_slider = slider(bind=scale, minval=0, maxval=1, value=0.01)

dt_slider_text = wtext(text="{:1.2f}".format(dt_scalar_slider.value * 10))


def animate_orbit_3d(r0, T, dt):
    global time_sim, time_display, dt_scalar
    ball = sphere(
    pos=vec(*r0) / SCALE, radius=0.3, color=color.white, make_trail=True, trail_radius=0.02, retain=50)
    earth = sphere(pos=vec(0, 0, 0), radius=6378e3 / SCALE, texture=textures.earth)
    # Set background color and center of view
    scene.background = color.black
    scene.fullscreen = True
    r = np.array(r0) @ rotation_x_matrix
    v = np.array([0, 0, v0]) @ rotation_x_matrix
    while True:
        rate(60)
        dt_eff = dt * dt_scalar
        #Update the total elapsed time in seconds
        time_sim += float(dt_eff)
        #Calculate earths rotation based on elapsed time in seconds
        earth.rotate(angle=2*np.pi/86400 * dt_eff, axis=vec(0, 1, 0))
        #Update the elapsed time widget text
        time_display.text = f"Elapsed time: {str(datetime.timedelta(seconds=time_sim))}"
        if follow_satellite:
            scene.follow(ball)
        else:
            scene.follow(None)
            scene.center = earth.pos

        a = acceleration(r)  # old acceleration
        r_new = (
            r + v * dt_eff + 0.5 * a * dt_eff**2
        )  # update the new position with the guess from the old acceleration
        a_new = acceleration(
            r_new
        )  # get new acceleration with the new guessed position
        v_new = v + 0.5 * (a + a_new) * dt_eff  # calculate new velocity
        # Update the radius and velocity variables
        r = r_new
        v = v_new
        # change the satellite position
        ball.pos = vec(*r_new) / SCALE

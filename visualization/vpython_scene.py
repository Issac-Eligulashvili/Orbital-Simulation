import numpy as np
from fontTools.subset import retain_empty_scripts
from vpython import sphere, vec, rate, color, scene, textures, checkbox, wtext, slider
from physics.motion import calculate_movement
from data.constants import v0, i, mu, gravitational_constant
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
#Set the rotation matrix based on the angle of inclination
rotation_x_matrix = np.array([[1,0,0],[0,np.cos(i), -np.sin(i)], [0,np.sin(i), np.cos(i)]])
#Spacer
wtext(text="\n\n")
#Display elapsed time
time_display = wtext(text="Elapsed time: 0s")
#Spacer
wtext(text="\n\n")
#Set the slider for the speed of the animation
dt_scalar = 1
min_value = 0.25 #minimum value of slider
max_value = 10 # Maximum value of slider
def scale(evt):
    global dt_scalar
    dt_scalar = min_value + (max_value - min_value) * evt.value #Map true value based on 0-1 value of slider
    dt_slider_text.text = "{:1.2f}".format(dt_scalar) #Update text

dt_scalar_slider = slider(bind=scale, minval=0, maxval=1, value=0.1)

dt_slider_text = wtext(text="{:1.2f}".format(dt_scalar_slider.value * 10))

planets = [
    {
        "position": [0,0,0],
        'mu': mu,
        "id": 0
    }
    # {
    #     "position": [0,0,0],
    #     'mu': gravitational_constant * 7.34767309e22, #calculate the mu of the planet/moon based on mass
    #     "id": 1
    # }
]

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

        #Calculate number of steps for sub-stepping
        steps = int(np.ceil(dt_eff / dt))
        sub_dt = dt_eff / steps


        for _ in range(steps):
            r,v = calculate_movement(r,v,sub_dt,None, planets)



        # change the satellite position
        ball.pos = vec(*r) / SCALE


import numpy as np
from fontTools.subset import retain_empty_scripts
from vpython import sphere, vec, rate, color, scene, textures, checkbox, wtext, slider, arrow
from physics.motion import calculate_movement
from data.constants import v0_sat, i, mu, gravitational_constant
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

i_sat = np.radians(i)

#Get the amount of simulated time passed in seconds
time_sim = 0.0
#Set the rotation matrix based on the angle of inclination
def getXRotationMatrix(deg):
    return np.array([[1,0,0],[0,np.cos(deg), -np.sin(deg)], [0,np.sin(deg), np.cos(deg)]])
sat_rotation_matrix = getXRotationMatrix(i_sat)
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
    },
    {
        "position": [3.84e8,0,0],
        'mu': gravitational_constant * 7.34767309e22, #calculate the mu of the planet/moon based on mass
        "id": 1
    }
]
# Draw plane vectors to debug
arrow(pos=vec(0,0,0), axis=vec(1 * 6378e4 / SCALE ,0,0), color=color.red, shaftwidth=0.05)   # +X (red)
arrow(pos=vec(0,0,0), axis=vec(0,1 * 6378e4 / SCALE,0), color=color.green, shaftwidth=0.05) # +Y (green)
arrow(pos=vec(0,0,0), axis=vec(0,0,1 * 6378e4 / SCALE), color=color.blue, shaftwidth=0.05)  # +Z (blue)

def animate_orbit_3d(r0_sat, T, dt):
    global time_sim, time_display, dt_scalar
    # Initialize the satellite sphere
    satellite = sphere(pos=vec(*r0_sat) / SCALE, radius=0.3, color=color.white, make_trail=True, trail_radius=0.02, retain=50)
    # Initialize earth sphere
    earth = sphere(pos=vec(0, 0, 0), radius=6378e3 / SCALE, texture=textures.earth)
    # Initialize moon sphere
    moon=sphere(pos=vec(3.84e8,0,0) / SCALE, radius=1738e3 / SCALE, texture = textures.stones)

    # Set background color and center of view
    scene.background = color.black
    scene.fullscreen = True

    #Set the radius and velocity vectors after rotation for satellite
    r_sat = sat_rotation_matrix @ np.array(r0_sat)
    v_sat = sat_rotation_matrix @ np.array([0, v0_sat, 0])

    # Get the rotation matrix for the moon
    moon_rotation_matrix = getXRotationMatrix(5.15)

    # Orbital parameters for the moon
    e_moon = 0.055
    a_moon = 3.84e8 / (1-e_moon)
    v0_moon = np.sqrt(mu * ((2 / 3.84e8) - (1 / a_moon)))

    #Set the radius and velocity vectors after rotation for the moon
    r_moon = np.array([3.84e8,0,0]) @ moon_rotation_matrix
    v_moon = np.array([0, v0_moon, 0]) @ moon_rotation_matrix

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
            scene.follow(satellite)
        else:
            scene.follow(None)
            scene.center = earth.pos

        #Calculate number of steps for sub-stepping
        steps = int(np.ceil(dt_eff / dt))
        sub_dt = dt_eff / steps


        for _ in range(steps):
            r_sat,v_sat = calculate_movement(r_sat,v_sat,sub_dt,None, planets)
            r_moon,v_moon = calculate_movement(r_moon,v_moon,sub_dt,1, planets)

        # change the satellite position
        satellite.pos = vec(*r_sat) / SCALE
        moon.pos = vec(*r_moon) * 0.15 / SCALE #Scale the visual distance of the moon so that its visible while keeping math accurate


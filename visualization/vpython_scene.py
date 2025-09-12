import numpy as np
from vpython import sphere, vec, rate, color, scene, textures, checkbox, wtext, slider
from physics.motion import calculate_movement
import datetime

def initialize_scene(cfg, r0_sat, dt):

    unit_scale = 1e6  # 1 unit = 1,000 km

    #UI State
    follow_satellite = {"value": False}

    def toggle_follow_satellite(evt):
        follow_satellite["value"] = evt.checked

    checkbox(bind=toggle_follow_satellite, text="Follow Satellite", checked=False)

    wtext(text="\n\n")
    # Display elapsed time
    time_display = wtext(text="Elapsed time: 0s")
    # Spacer
    wtext(text="\n\n")

    dt_scalar = {"value": 1.0}
    min_value = 0.25  # minimum value of slider
    max_value = 10  # Maximum value of slider

    def scale(evt):
        nonlocal  dt_scalar
        dt_scalar["value"] = min_value + (max_value - min_value) * evt.value  # Map true value based on 0-1 value of slider
        dt_slider_text.text = "{:1.2f}".format(dt_scalar["value"])  # Update text

    dt_scalar_slider = slider(bind=scale, minval=0, maxval=1, value=0.1)
    dt_slider_text = wtext(text="{:1.2f}".format(dt_scalar_slider.value * 10))

    # Scene Objects

    planets = [
        {
            "position": [0, 0, 0],
            'mu': cfg.mu,
            "id": 0
        },
        {
            "position": [3.84e8, 0, 0],
            'mu': cfg.GRAVITATIONAL_CONSTANT * 7.34767309e22,  # calculate the mu of the planet/moon based on mass
            "id": 1
        }
    ]

    # Initialize the satellite sphere
    satellite = sphere(pos=vec(*r0_sat) / unit_scale, radius=0.3, color=color.white, make_trail=True, trail_radius=0.02,
                       retain=50)
    # Initialize earth sphere
    earth = sphere(pos=vec(0, 0, 0), radius=6378e3 / unit_scale, texture=textures.earth)
    # Initialize moon sphere
    moon = sphere(pos=vec(3.84e8, 0, 0) / unit_scale, radius=1738e3 / unit_scale, texture=textures.stones)

    # Get the inclination in radians
    i_sat = np.radians(cfg.i)

    # Set the rotation matrix based on the angle of inclination
    def get_rotation_matrix(rad):
        return np.array([[1, 0, 0],
                         [0, np.cos(rad), -np.sin(rad)],
                         [0, np.sin(rad), np.cos(rad)]])

    sat_rotation_matrix = get_rotation_matrix(i_sat)

    # Set the radius and velocity vectors after rotation for satellite
    r_sat = np.array(r0_sat)
    v_sat = sat_rotation_matrix @ np.array([0, 0, cfg.v0_sat])

    # Get the rotation matrix for the moon
    moon_rotation_matrix = get_rotation_matrix(np.radians(5.15))

    # Orbital parameters for the moon
    e_moon = 0.055
    a_moon = 3.84e8 / (1 - e_moon)
    v0_moon = np.sqrt(cfg.mu * ((2 / 3.84e8) - (1 / a_moon)))

    # Set the radius and velocity vectors after rotation for the moon
    r_moon = np.array([3.84e8, 0, 0])
    v_moon = moon_rotation_matrix @ np.array([0, v0_moon, 0])

    return {
        "cfg": cfg,
        "dt": dt,
        "time_sim": 0.0,
        "follow_satellite": follow_satellite,
        "dt_scalar": dt_scalar,
        "time_display": time_display,
        "earth": earth,
        "satellite": satellite,
        "moon": moon,
        "r_sat": r_sat,
        "v_sat": v_sat,
        "r_moon": r_moon,
        "v_moon": v_moon,
        "planets": planets,
        "unit_scale": unit_scale,
    }

def step_orbit(state):
    rate(60)

    dt_eff = state["dt"] * state["dt_scalar"]["value"]
    state["time_sim"] += dt_eff

    # Earth Rotation
    state["earth"].rotate(angle=2*np.pi/86400 * dt_eff, axis=vec(0, 1, 0))
    state["time_display"].text = f"Elapsed time: {str(datetime.timedelta(seconds=state['time_sim']))}"

    if state["follow_satellite"]["value"]:
        scene.follow(state["satellite"])
    else:
        scene.follow(None)
        scene.center = state["earth"].pos

    # Calculate number of steps for sub-stepping
    steps = int(np.ceil(dt_eff / state["dt"]))
    sub_dt = dt_eff / steps

    for _ in range(steps):
        state["r_sat"], state["v_sat"] = calculate_movement(state["r_sat"], state["v_sat"], sub_dt, None, state["planets"])
        state["r_moon"], state["v_moon"] = calculate_movement(state["r_moon"], state["v_moon"], sub_dt, 1, state["planets"])

    # Update the visuals of the sim
    state["satellite"].pos = vec(*state["r_sat"]) / state["unit_scale"]
    state["moon"].pos = vec(*state["r_moon"]) * 0.15 / state["unit_scale"]


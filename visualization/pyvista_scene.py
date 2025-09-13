import pyvista as pv
from pyvista import examples
import numpy as np
from physics.motion import calculate_movement
import time

def initialize_scene(cfg, r0_sat, dt):
    unit_scale = 1e6  # 1 unit = 1,000 km
    # Create sphere and plotter
    plotter = pv.Plotter()
    plotter.set_background("black")  # or (0, 0, 0)
    satellite = pv.Sphere(radius=0.5, center=((np.array(r0_sat) / unit_scale).tolist()))
    earth_mesh = examples.planets.load_earth(radius=6378e3 / unit_scale)


    # Add sphere to scene
    actor = plotter.add_mesh(satellite, color='white')
    earth_texture = examples.load_globe_texture()
    earth_actor = plotter.add_mesh(earth_mesh, texture=earth_texture)
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

    # Get the inclination in radians
    i_sat = np.radians(cfg.i)

    # Set the rotation matrix based on the angle of inclination
    def get_rotation_matrix(rad):
        return np.array([[np.cos(rad), -np.sin(rad), 0],
                     [np.sin(rad),  np.cos(rad), 0],
                     [0,            0,           1]])

    sat_rotation_matrix = get_rotation_matrix(i_sat)

    # Animation parameters
    position = r0_sat

    # Define orbital plane normal (before inclination)
    orbital_normal = np.array([0, 0, 1])  # Initially equatorial

    # Apply inclination to the orbital normal
    rotated_normal = sat_rotation_matrix @ orbital_normal

    # Position vector
    r_vec = np.array(r0_sat)

    # Velocity is perpendicular to both position and orbital normal
    v_direction = np.cross(rotated_normal, r_vec)
    v_direction = v_direction / np.linalg.norm(v_direction)

    # Scale by velocity magnitude
    velocity = cfg.v0_sat * v_direction
    return {
        "cfg": cfg,
        "plotter": plotter,
        "actor": actor,
        "r_sat": position,
        "v_sat": velocity,
        "dt": dt,
        "planets": planets,
        "unit_scale": unit_scale,
        "time_sim": 0.0,
        "satellite": satellite,
    }

def step_animation(state):

    dt_eff = state["dt"]
    state["time_sim"] += dt_eff

    # Calculate number of steps for sub-stepping
    steps = int(np.ceil(dt_eff / state["dt"]))
    sub_dt = dt_eff / steps

    for _ in range(steps):
        state["r_sat"], state["v_sat"] = calculate_movement(state["r_sat"], state["v_sat"], sub_dt, None,
                                                            state["planets"])
    # Compute new scaled position
    new_pos_scaled = np.array(state["r_sat"]) / state["unit_scale"]

    # Move satellite to new position
    state["satellite"].points = state["satellite"].points - state["satellite"].center + new_pos_scaled

    state["plotter"].update()
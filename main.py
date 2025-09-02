from visualization.madplotlib_scene import simulate_orbit, animate_orbit
from data.constants import corrected_rad

positions = simulate_orbit([corrected_rad, 0], 6000, 1)
animate_orbit(positions)

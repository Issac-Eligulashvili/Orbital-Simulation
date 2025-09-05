from visualization.madplotlib_scene import simulate_orbit, animate_orbit
from data.constants import r0_m, T

positions = simulate_orbit([r0_m, 0], T, 20)


animate_orbit(positions)

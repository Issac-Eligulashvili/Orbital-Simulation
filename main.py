from visualization.madplotlib_scene import simulate_orbit, animate_orbit
from data.constants import r0_m

positions = simulate_orbit([r0_m, 0], 6000, 20)


animate_orbit(positions)

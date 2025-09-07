import numpy as np

# Set Initial Place of Sattelite
isApogee = False
isPerigee = True
# Mass of planet in kilograms
planetary_mass = 5.972e24
# Radius of the planet in kilometers
planetary_radius = 6378
# Newtons Gravitational Constant
gravitational_constant = 6.67e-11
# Starting Distance from Planet in kilometers
distance = 3000
# Corrected Radius
r0 = planetary_radius + distance
# Corrected Radius in meters
r0_m = r0 * 1000
# Gravitational Paramater
mu = planetary_mass * gravitational_constant
# Eccentricity
e = 0.6
# Semi-Major Axis in m
a = 0
if isApogee:
    a = r0_m / (1 + e)
elif isPerigee:
    a = r0_m / (1 - e)
# Initial Velocity based on semi-major axis and eccentricity
v0 = np.sqrt(mu * ((2 / r0_m) - (1 / a)))
# Period of orbit
T = 2 * np.pi * np.sqrt(a**3 / mu)

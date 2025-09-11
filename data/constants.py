import numpy as np

class Config:
    def __init__(self):
        # Set Initial Place of Satellite
        self.STARTING_LOCATION = "perigee"
        # Mass of planet in kilograms
        self.PLANETARY_MASS = 5.972e24
        # Radius of the planet in kilometers
        self.PLANETARY_RADIUS = 6378
        # Newtons Gravitational Constant
        self.GRAVITATIONAL_CONSTANT = 6.67e-11
        # Starting Distance from Planet in kilometers
        self.DISTANCE = 3000
        # Eccentricity
        self.e = 0.6
        # Inclination of orbit in degrees
        self.i = 0
        # Control the state of the animation
        self.running = True
    @property
    # Corrected Radius
    def r0(self):
        return self.PLANETARY_RADIUS + self.DISTANCE
    @property
    def r0_m(self):
    # Corrected Radius in meters
        return self.r0 * 1000
    @property
    def mu(self):
    # Gravitational Parameter
        return self.PLANETARY_MASS * self.GRAVITATIONAL_CONSTANT
    @property
    def a(self):
    # Semi-Major Axis in m
        if self.STARTING_LOCATION == "perigee":
            return self.r0_m / (1 - self.e)
        else:
            return self.r0_m / (1 + self.e)
    @property
    def v0_sat(self):
    # Initial Velocity based on semi-major axis and eccentricity
        return np.sqrt(self.mu * ((2 / self.r0_m) - (1 / self.a)))
    @property
    # Period of orbit
    def T(self):
        return  2 * np.pi * np.sqrt(self.a ** 3 / self.mu)

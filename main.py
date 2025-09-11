from visualization.vpython_scene import animate_orbit_3d
from data.constants import Config

cfg = Config()

animate_orbit_3d([cfg.r0_m, 0, 0], cfg.T, 20, cfg)

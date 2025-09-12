import atexit

from visualization.vpython_scene import step_orbit, initialize_scene
from data.constants import Config

Config.clear_flag()
cfg = Config()


state = initialize_scene(cfg, [cfg.r0_m, 0, 0], 20)

while Config.is_running():
    step_orbit(state)

atexit.register(Config.clear_flag())

import atexit, os
import time

from visualization.pyvista_scene import initialize_scene, step_animation
from data.constants import Config
from data.config_instance import cfg

Config.clear_running_flag()
Config.clear_image_flag()

state = initialize_scene(cfg, [cfg.r0_m, 0, 0], 20)
state["plotter"].show(auto_close=False, interactive_update=True)

def start():
    while Config.is_running():
            step_animation(state)
            time.sleep(0.001)

start()


atexit.register(Config.clear_running_flag)

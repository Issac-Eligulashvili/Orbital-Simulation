from data.constants import Config
from visualization.pyvista_scene import capture_image
import time
from data.config_instance import cfg

def set_image():
    Config.enable_save()
    print("Enabled Save")
    time.sleep(cfg.IMAGE_CAPTURE_TIME)
    Config.disable_save()
    print("Disabled Save")

set_image()

# def stop_animation():
#     print("Stopping animation...")
#     Config.stop()

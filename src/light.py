import time
import board
import neopixel
import config
import lifx

class LightSwitch:
    def __init__(self):
        self.color = None
        self.temperature = None
        self.brightness = None
        self.last_motion = time.monotonic()

    def motion(self):
        self.last_motion = time.monotonic()

    def update(self):
        # Check if motion was detected in the last 5 minutes
        if time.monotonic() - self.last_motion > config.motion_timeout:
            lifx.power_off()
            
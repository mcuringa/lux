import time
import board
import analogio
import utils
from utils import debounce

import config
from config import lifx

hues = {
    "red": 0,
    "red_orange": 15,
    "orange": 30,
    "yellow_orange": 45,
    "gold": 50,
    "yellow": 60,
    "chartreuse": 75,
    "yellow_green": 90,
    "green": 120,
    "spring_green": 150,
    "turquoise": 165,
    "cyan": 180,
    "sky_blue": 200,
    "azure": 210,
    "blue": 240,
    "deep_blue": 255,
    "indigo": 270,
    "violet": 285,
    "purple": 300,
    "magenta": 315,
    "rose": 340,
    "crimson": 350,
}


utils.connect_wifi()
requests = utils.get_requests()
base = "https://api.lifx.com/v1/lights"

def __post(payload):
    url = f"{base}/id:{lifx.light_id}/state"
    headers = {
        "accept": "text/plain",
        "content-type": "application/json",
        "Authorization": f"Bearer {lifx.key}"
    }
    response = requests.put(url, json=payload, headers=headers)
    return response.json()


def get_lights():
    response = requests.get("{base}/all", auth=(lifx.key, ""))
    return response.json()

def toggle():
    response = requests.post(
        f"{base}/id:{lifx.light_id}/toggle", auth=(lifx.key, ""))
    return response.json()

def power_on():
    return __post({"power": "on"})

def power_off():
    return __post({"power": "off"})


def set_color(hue, sat=.8):
    if hue in hues:
        hue = hues[hue]
    color = f"hue:{hue} saturation:{sat}"
    payload = {
        "duration": 1,
        "fast": False,
        "color": color
    }
    return __post(payload)


def set_brightness(brightness):
    payload = {
        "duration": 1,
        "fast": False,
        "brightness": float(brightness/100)
    }
    return __post(payload)


def stop_effects():
    print("stopping effect")
    url = f"{base}/id:{lifx.light_id}/effects/off"
    headers = {"Authorization": f"Bearer {lifx.key}"}
    return requests.post(url, headers=headers).json()


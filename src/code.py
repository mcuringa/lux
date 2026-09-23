import time
import board
import neopixel
# from tests import lifx_test

import supervisor

supervisor.runtime.autoreload = False

print("testing wifi")
import utils
requests = utils.get_requests()
print(requests.get("https://example.com").text)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
print("up and running")
# pixels.fill((0, 255, 0))
# time.sleep(3)
# print("testing wifi and lifx")
# lifx_test.test()
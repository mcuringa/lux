import time
import board
import neopixel



print("hello world")

# flash the noboard neopixel 5 times then go solid green
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
for i in range(5):
    pixels.fill((255, 0, 0))
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    time.sleep(0.5)
pixels.fill((0, 255, 0))
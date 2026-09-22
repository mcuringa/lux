import time
import board
import neopixel



print("hello world")

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
# run through 50 different colors with a very short delay
for i in range(50):
    pixels.fill((i * 5, 255 - i * 5, i * 2))
    time.sleep(0.03)

print("up and running")
pixels.fill((0, 255, 0))
time.sleep(120)
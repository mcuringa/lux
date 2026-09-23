"""Run on CircuitPython with `import lifx_test` from a fresh REPL.

Requires the usual generated config.py and device libraries. Watch the light
and serial output; this changes its state and leaves it on at 100% brightness.
"""

import time

import utils


print("Connecting to Wi-Fi...")
utils.connect_wifi()

# lifx creates its requests session at import time, after Wi-Fi is connected.
import lifx


VISUAL_WAIT = 4
failures = []


def run_test(label, function, *args, wait=VISUAL_WAIT):
    print("\nTEST:", label)
    try:
        response = function(*args)
        print("Response:", response)
        if isinstance(response, dict):
            if response.get("error") or response.get("errors"):
                raise RuntimeError("LIFX returned an error")
            for result in response.get("results", []):
                if result.get("status") != "ok":
                    raise RuntimeError("LIFX reported an unsuccessful result")
        print("Request completed; check the response above.")
    except Exception as error:
        failures.append(label)
        print("FAILED:", error)
    if wait:
        print("Watch the light for", wait, "seconds...")
        time.sleep(wait)

def test():
    requests = utils.get_requests()
    print("Testing wifi")
    print(requests.get("https://example.com").text)

    run_test("get_lights: list available lights", lifx.get_lights, wait=0)

    # Only check the request; no active effect is needed for this test.
    run_test("stop_effects: request should succeed", lifx.stop_effects, wait=0)

    run_test("power_on: light should turn on", lifx.power_on)
    run_test("set_brightness: 100%", lifx.set_brightness, 100)
    run_test("power_off: light should turn off", lifx.power_off)
    run_test("toggle: light should turn on", lifx.toggle)
    run_test("toggle: light should turn off", lifx.toggle)
    run_test("power_on: light should turn on again", lifx.power_on)

    for name in lifx.hues:
        run_test("set_color: " + name, lifx.set_color, name)

    for brightness in (25, 50, 100):
        run_test(
            "set_brightness: {}%".format(brightness),
            lifx.set_brightness,
            brightness,
        )

    print("\nTests finished. Confirm the visible changes matched the messages.")
    if failures:
        print("Failed requests:", ", ".join(failures))
    else:
        print("No request errors detected.")

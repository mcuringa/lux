import wifi
import config
import adafruit_requests
import socketpool



def connect_wifi(timeout=15):
    if not wifi.radio.connected:
        print("Connecting to Wi-Fi...")
        print("SSID:", config.wifi.ssid)
        print("Password:", config.wifi.password)
        wifi.radio.connect(
            config.wifi.ssid,
            config.wifi.password,
            timeout=timeout,
        )
        print("Connected!")
        print("IP address:", wifi.radio.ipv4_address)


def get_requests():
    connect_wifi()
    pool = socketpool.SocketPool(wifi.radio)
    return adafruit_requests.Session(pool)


def debounce(f, delay):
    last_call = 0

    def wrapper(*args, **kwargs):
        nonlocal last_call
        now = time.monotonic()
        if now - last_call >= delay:
            last_call = now
            return f(*args, **kwargs)
    return wrapper

Welcome to lux
==============
`lux` is the software for our DIY smart light switch.
It runs oncircuitpython and an adafruit qtpy. You configure 
your settings (wifi, etc) in `config.json`, push your changes
to your qtpy, and then `lux` will run your light switch.

_This guide assumes you have already built the hardware switch._

Features
--------
The smart switch features:
- Hardware on/off button.
- Status lights
- Proximity sensor (with programmable behavior)
- Color slider to change the **color** of the light
- Temperature slider to change the **temperature** of white light
- Dimmer knob to change the **brightness** of the light
- Four programmable buttons to run custom routines (e.g. bright white, theater mode, etc)


Configuration
-------------
Change these settings in `config.json` to configure your light switch.
You **must** set the wifi `ssid` and `wifi_password` to connect to your network. 
Other settings are optional and override the defaults.

- ssid: the wifi ssid to connect to
- wifi_password: the wifi password to connect to
- light_timeout: turn off the light after this many seconds of inactivity
- night: a string (hh:mm) representing the time of day the light considers night time. Use a 24 hour clock. For example, "22:30" is 10pm.
- morning: a string (hh:mm) representing the time of day the light considers morning. Use a 24 hour clock. For example, "06:30" is 6:30am.

Install and setup
-----------------
You do not have to write any code to use `lux`, but you will need
to set up your python environment so that you can configure your
local light switch. The basic steps are:

1. Download and unzip (or clone) the project from github at: <tbd>. From the terminal, move into the project directory.
2. Run `lux.sh`. This will:
   - install python for your computer if needed (along with other python requirements)
   - create a virtual environment in the `venv` directory
   - install the required python packages into the virtual environment
     - `pip install -r requirements.txt` or `uv pip install -r requirements.txt` depending on your setup
3. Activate the virtual environment by running `source venv/bin/activate` (on linux or mac) or `venv\Scripts\activate` (on windows). You should see `(venv)` in your terminal prompt.
3. In the python environment in the, run `invoke install`. This will install the required packages on your 
   set up local configuration files and provide further instructions if you need system installs.


Pushing your changes
---------------------
After you make changes to `config.json` or write custom routines (e.g. for buttons):

1. Connect your qtypy to your computer via USB.
2. Run `invoke push`. This will copy your changes to the qtpy and restart the light switch.
   You should see the light switch start up and connect to your wifi network.



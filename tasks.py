from pathlib import Path
import os
import shutil
import subprocess
import requests
import json
import tomllib

from invoke import task


def default_config() -> str:
    """
    Default configuration for the project.
    """

    return """
[wifi]
ssid = "YOUR WIFI NAME"
password = "WIFI PASSWORD"


[lifx]
# your lifx API key can be found here: https://cloud.lifx.com/settings
key = "YOUR LIFX API KEY"

# the lifx light you want to control, can be found here: https://api.lifx.com/v1/lights/all
# or run `invoke lights` to see all of the lights connected to your API key
light_id = "YOUR LIFX LIGHT ID"


# sensor config
# temperature_offset = -5
# sea_level_pressure = 1013.25
    
    """


def get_config() -> dict:
    """Get the configuration from the config.toml file."""
    config_path = Path("./config.toml")
    if not config_path.exists():
        raise FileNotFoundError(f"Could not find config.toml at {config_path}")
    with config_path.open("rb") as f:
        config = tomllib.load(f)
    return config


def find_circuitpy() -> Path:
    """Find the mount point for the CIRCUITPY volume."""
    candidates = []

    config = get_config()
    config_path = config.get("CIRCUITPY")
    if config_path:
        candidates.append(Path(config_path))

    # get linux paths
    user = os.environ.get("USER")
    if user:
        candidates.extend(
            [
                Path("/media") / user / "CIRCUITPY",
                Path("/run/media") / user / "CIRCUITPY",
            ]
        )
    # add macOS path
    candidates.append(Path("/Volumes/CIRCUITPY"))

    # add default Windows path
    candidates.append(Path("C:/CIRCUITPY"))

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            print(f"CIRCUITPY mounted at {candidate}")
            return candidate

    searched = ", ".join(str(candidate) for candidate in candidates)
    raise ValueError(
        "Could not find the CIRCUITPY volume. "
        "Set CIRCUITPY=/path/to/CIRCUITPY or pass --circuitpy. "
        f"Searched: {searched}"
    )


@task
def config(ctx):
    def emit(data, indent=0):
        lines = []
        pad = " " * indent

        # Values first
        for key, value in data.items():
            if not isinstance(value, dict):
                lines.append(f"{pad}{key} = {value!r}")

        # Sections become namespace classes
        for key, value in data.items():
            if isinstance(value, dict):
                if lines:
                    lines.append("")
                lines.append(f"{pad}class {key}:")
                body = emit(value, indent + 4)
                lines.extend(body or [f"{pad}    pass"])

        return lines

    py_file = Path("./src/config.py")
    config = get_config()

    output = [
        "# Generated from config.toml -- do not edit.",
        "",
        *emit(config),
        "",
    ]

    py_file.write_text("\n".join(output))

@task
def lights(ctx, v=False):
    base = "https://api.lifx.com/v1/lights"
    config = get_config()
    response = requests.get(f"{base}/all", auth=(config["lifx_key"], ""))
    x = response.json()
    if v:
        print(json.dumps(x, indent=4))
        return

    for light in x:
        print(f"""
Light: {light['label']}
ID: {light['id']}
        """)

@task
def push(ctx):
    """Copy config.json into src and all src python files into CIRCUITPY."""
    del ctx
    print("Pushing config.json and src/*.py files to CIRCUITPY...")
    circuitpy_path = find_circuitpy()

    # copy config.json to CIRCUITPY
    shutil.copy2("config.json", circuitpy_path / "config.json")
    # copy all .py files from src to CIRCUITPY
    for py_file in Path("src").glob("*.py"):
        shutil.copy2(py_file, circuitpy_path / py_file.name)
    print("Pushed config.json and src/*.py files to CIRCUITPY.")

@task(name="circ-libs")
def circ_libs(ctx):
    """Install CircuitPython libraries from requirements-circuitpython.txt."""
    del ctx

    libs = []
    with open("requirements-circuitpython.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                libs.append(line)

    circup = shutil.which("circup")
    circuitpy_path = find_circuitpy()

    print(f"Installing CircuitPython libraries to {circuitpy_path}...")
    print(f"Libraries to install: {'\n\t'.join(libs)}")
    subprocess.run(
        [circup, "--path", str(circuitpy_path), "install", *libs],
        check=True,
    )

@task
def install(ctx):
    """Install the required python packages into the virtual environment."""
    del ctx
    print("Creating default config.toml")
    config_path = Path("config.toml")
    if not config_path.exists():
        config_path.write_text(default_config())
        print("Created default config.toml")


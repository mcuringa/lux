from pathlib import Path
import os
import shutil
import subprocess
import requests

from invoke import task
import json

def get_config() -> dict:
    """Get the configuration from the config.json file."""
    config_path = Path("./config.json")
    if not config_path.exists():
        raise FileNotFoundError(f"Could not find config.json at {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)


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

# -*- coding: utf-8 -*-
"""Combine all constraints*.txt into one constraints.txt.
"""
import os
import sys
from collections import defaultdict
from pathlib import Path

MAIN_DIR = Path(os.path.dirname(__file__)) / os.pardir


def parse_file(filename):
    if not filename.exists():
        print(f"ERROR: {filename} does not exist.")
        sys.exit(1)
    print(f"Parsing {os.path.realpath(filename)}")
    mapping = {}
    with filename.open() as myfile:
        for line in myfile.read().splitlines():
            if "==" not in line:
                continue
            package, version = line.split("==")
            mapping[package] = version
    return mapping


constraints = MAIN_DIR / "constraints.txt"
c38 = parse_file(MAIN_DIR / "venvs" / "38" / "constraints.txt")
c39 = parse_file(MAIN_DIR / "venvs" / "39" / "constraints.txt")
c310 = parse_file(MAIN_DIR / "venvs" / "310" / "constraints.txt")
c311 = parse_file(MAIN_DIR / "venvs" / "311" / "constraints.txt")

# Gather them all in one dictionary.
pins = defaultdict(dict)
for package, version in c38.items():
    pins[package][38] = version
for package, version in c39.items():
    pins[package][39] = version
for package, version in c310.items():
    pins[package][310] = version
for package, version in c311.items():
    pins[package][311] = version

# Combine them.
combi = []
for package, versions in pins.items():
    py38_version = versions.pop(38, None)
    py39_version = versions.pop(39, None)
    py310_version = versions.pop(310, None)
    py311_version = versions.pop(311, None)
    if py38_version == py39_version == py310_version == py311_version:
        # All versions are the same.
        combi.append(f"{package}=={py311_version}")
        continue
    # Some versions are different or missing.
    # Start with the lowest Python.
    # Check if Python 3.8 differs from the rest.
    if py38_version is not None:
        combi.append(f'{package}=={py38_version}; python_version == "3.8"')

    # Check if Python 3.9 differs from the rest.
    if py39_version == py310_version == py311_version and py39_version is not None:
        combi.append(f'{package}=={py39_version}; python_version >= "3.9"')
        continue
    if py39_version is not None:
        combi.append(f'{package}=={py39_version}; python_version == "3.9"')

    # Check if Python 3.10 differs from the rest.
    if py310_version == py311_version and py310_version is not None:
        combi.append(f'{package}=={py310_version}; python_version >= "3.10"')
        continue
    if py310_version is not None:
        combi.append(f'{package}=={py310_version}; python_version == "3.10"')

    # Check if Python 3.11 differs from the rest.
    if py311_version is not None:
        combi.append(f'{package}=={py311_version}; python_version >= "3.11"')

output = "\n".join(combi) + "\n"
# sanity check:
assert "==None" not in output
with open(constraints, "w") as myfile:
    myfile.write(output)
print(
    f"Wrote combined constraints for all Python versions to {os.path.realpath(constraints)}."
)

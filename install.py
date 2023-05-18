"""Create virtualenv (if it does exist yet) and pip-install Plone and friends.
This is a script for core Plone development.

Usage:

Call this with one of the following extras defined in pyproject.toml:

* core (Plone)
* buildout (zc.buildout + extensions + recipes)
* test (test extras for all Plone packages)
* ecosystem (Mosaic, PrintingMailHost, etc)

To install multiple, separate by only commas, no spaces.

Special:

* default (same as: core,buildout,test,ecosystem)
* full (every package that is defined in constraints.txt)
* ranges (every package that is defined in ranges.txt, updated eagerly)

Look in the scripts directory for more scripts.
"""
import os
import subprocess
import sys
import venv

# Make sure we have a virtualenv with pip.
if not os.path.exists("bin/pip"):
    venv.create(".", with_pip=True)

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)


def run(command, **kwargs):
    return subprocess.run(command, check=True, **kwargs)


# Directory where this file is.
MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
EXTRAS = sys.argv[-1]

if EXTRAS == "default":
    EXTRAS = "core,buildout,test,ecosystem"
print("Installing base requirements (mainly pip, setuptools, zc.buildout when needed.")
if "full" in EXTRAS or "buildout" in EXTRAS or "ranges" in EXTRAS:
    # The extras contain buildout.
    req = f"{MAIN_DIR}/requirements-buildout.txt"
else:
    req = f"{MAIN_DIR}/requirements.txt"
run(["./bin/pip", "install", "-r", req])

print("Installing/updating the requested packages.")
if EXTRAS == "full":
    print("Explicitly installing every package in constraints.txt")
    run(["./bin/pip", "install", "-r", f"{MAIN_DIR}/constraints.txt"])
elif EXTRAS == "ranges":
    print("Eagerly upgrading to newer versions for all packages in ranges.txt.")
    run(
        [
            "./bin/pip",
            "install",
            "-U",
            "--upgrade-strategy",
            "eager",
            "-r",
            f"{MAIN_DIR}/ranges.txt",
        ]
    )
else:
    run(["./bin/pip", "install", f".[{EXTRAS}]", "-c", f"{MAIN_DIR}/constraints.txt"])

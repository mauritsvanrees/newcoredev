import subprocess
import sys

try:
    # Python 3.11+
    import tomllib
except ImportError:
    # Python 3.10-
    import tomli as tomllib


CONSTRAINTS_FILE = "constraints.txt"
RANGES_FILE = "ranges.txt"
# Get our config.
with open("pyproject.toml", "rb") as myfile:
    # Example:
    # {'bugfix': [], 'major': ['certifi', 'pytz', 'trove-classifiers']}
    config = tomllib.load(myfile)["tool"]["plonecoredev"]
    major = config.get("major", [])
    feature = config.get("feature", [])
    bugfix = config.get("bugfix", [])
    default_target = config.get("default_target", "feature")
    allowed_default_targets = ["bugfix", "feature", "major"]
    if default_target not in allowed_default_targets:
        print(f"{default_target=} not in {allowed_default_targets=}")
        sys.exit(1)


def get_constraints():
    """Read constraints.txt.

    We return the list of constraints.
    """
    with open(CONSTRAINTS_FILE) as myfile:
        return myfile.read().splitlines()


def get_target(package):
    if package in major:
        return "major"
    if package in feature:
        return "feature"
    if package in bugfix:
        return "bugfix"
    return default_target


def get_range(pin):
    """Get a version range for the package.

    By default we allow feature releases.
    In project.toml in tool.plonecoredev we can define packages for which we
    only accept bugfixes or where major releases are fine.
    """
    if ";" in pin:
        # For example: backports.zoneinfo==0.2.1; python_version == "3.8"
        pin, marker = pin.split(";")
        return f"{get_range(pin)}; {marker}"

    package, version = pin.split("==")
    minimum = f"{package}>={version}"
    target = get_target(package)
    if target == "major":
        return minimum
    version_parts = version.split(".")
    if target == "feature":
        # package==1.2.3 -> package>=1.2.3, ==1.*
        return f"{minimum}, =={version_parts[0]}.*"
    # What is left, is bugfix only.
    # package==1.2.3 -> package>=1.2.3, ==1.2.*
    version_part = ".".join(version_parts[:2])
    return f"{minimum}, =={version_part}.*"


# Write the ranges file.
print(f"Writing {RANGES_FILE}")
with open(RANGES_FILE, "w") as myfile:
    for pin in get_constraints():
        dep = get_range(pin)
        myfile.write(f"{dep}\n")

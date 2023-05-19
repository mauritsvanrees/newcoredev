#! /bin/sh
# Pip freeze the installed packages into constraints.txt.
# Note that pip/setuptools/wheel are excluded by pip unless we call it with --all.
# We are happy to follow pip's lead here.
# We also exclude zc.buildout and our dummy plonecoredev package.
# And we exclude editable packages.
import os
import subprocess


process = subprocess.run(
    [
        "bin/pip",
        "freeze",
        "--exclude-editable",
        "--exclude",
        "plonecoredev",
        "--exclude",
        "zc.buildout",
    ],
    check=True,
    capture_output=True,
    text=True,
)
FILENAME = "constraints.txt"
with open(FILENAME, "w") as myfile:
    myfile.write("\n".join(sorted(process.stdout.splitlines(), key=str.lower)))
print(f"Wrote {os.getcwd()}/{FILENAME}")

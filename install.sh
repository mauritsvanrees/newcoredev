#!/bin/sh
if test $# -ne 1; then
    cat <<EOF
Create virtualenv (if it does exist yet) and pip-install Plone and friends.
This is a script for core Plone development.

Usage:

Call this with one of the following extras defined in pyproject.toml.

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
EOF
    exit
fi
if test ! -f bin/pip; then
    echo "Creating virtualenv..."
    `which python3.11` -m venv .
fi
EXTRAS=$1
if test $EXTRAS == "default"; then
    EXTRAS="core,buildout,test,ecosystem"
fi

echo "Installing base requirements (mainly pip, setuptools, zc.buildout when needed."
case $EXTRAS in
*full*|*buildout*|*ranges*)
    # The extras contain buildout.
    ./bin/pip install -r requirements-buildout.txt;;
*)
    ./bin/pip install -r requirements.txt;;
esac

echo "Installing/updating the requested packages."
case $EXTRAS in
full)
    echo "Explicitly installing every package in constraints.txt"
    ./bin/pip install -r constraints.txt;;
ranges)
    echo "Eagerly upgrading to newer versions for all packages in ranges.txt."
    ./bin/pip install -U --upgrade-strategy eager -r ranges.txt;;
*)
    ./bin/pip install .[$EXTRAS] -c constraints.txt;;
esac

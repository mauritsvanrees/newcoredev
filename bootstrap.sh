#!/bin/sh
`which python3.11` -m venv .
./bin/pip install -r requirements.txt
./bin/pip install .[core,buildout,test,ecosystem] -c constraints.txt

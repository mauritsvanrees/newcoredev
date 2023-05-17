#!/bin/sh
`which python3.11` -m venv .
./bin/pip install -r ../../requirements.txt
./bin/pip install ../../[core] -c ../../constraints.txt

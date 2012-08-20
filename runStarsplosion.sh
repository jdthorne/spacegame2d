#!/bin/bash

export PYTHONPATH=`find ./src/ -type d | grep -v 'playerdata' | tr '\n' ':'`

if [[ "$1" == "--profile" ]]; then
   pycallgraph src/app/Main.py   
else
   /usr/bin/python src/app/Main.py
fi

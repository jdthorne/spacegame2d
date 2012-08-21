#!/bin/bash

export PYTHONPATH=`find ./src/ -type d | grep -v 'playerdata' | tr '\n' ':'`

/usr/bin/python src/app/Main.py $*

#!/bin/bash

mode=$1
name=$2
cd /home/safronov/Projects/UDACHA/scripts/mixalime/
python3 launch_mixalime.py $mode
python3 build_release.py $mode $name
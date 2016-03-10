#!/bin/bash -x

# Get the location of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


pushd $DIR
./nmNightlyUpdate.py
popd

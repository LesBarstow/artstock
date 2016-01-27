#!/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
cd "$BASEDIR"

if [ ! -d "$BASEDIR/pyvirtenv" ]; then
    virtualenv "$BASEDIR/pyvirtenv"
fi

source $BASEDIR/pyvirtenv/bin/activate
if [ -f "$BASEDIR/requirements.txt" ]; then
    pip install -r "$BASEDIR/requirements.txt"
fi

if [ $# > 0 ]; then
    exec "$@"
fi
#!/bin/bash
# wrapper script to allow running of the reader by OS startup and other processes
# that are not going to activate the python venv themselves.

SCRIPTDIR=$(dirname "$0")
pushd $SCRIPTDIR

if [[ ! -d venv ]]; then
  >&2 echo run \'python3 -m venv venv\' in $SCRIPTDIR directory before calling $0
  exit 1
fi

venv/bin/python reader.py

#!/bin/bash

SCRIPTDIR=$(dirname "$0")
pushd $SCRIPTDIR

if [[ ! -d venv ]]; then
  >&2 echo run \'python3 -m venv venv\' in $SCRIPTDIR directory before calling $0
  exit 1
fi

venv/bin/python reader.py

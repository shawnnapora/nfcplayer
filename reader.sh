#!/bin/bash

SCRIPTDIR=$(dirname "$0")
if [[ ! -d $SCRIPTDIR/venv ]]; then
  >&2 echo run \'python3 -m venv venv\' in $SCRIPTDIR directory before calling $0
  exit 1
fi

source $SCRIPTDIR/venv/bin/activate
$SCRIPTDIR/reader.py

#!/usr/bin/env bash
set -ue

cd $(dirname $0)

# Find a python bin

if which python3 2>&1 >/dev/null; then
   PYTHON_CMD="python3"
elif which python 2>&1 >/dev/null; then
   PYTHON_CMD="python"
else
   echo Please install Python3 and relaunch this script >&2
   exit 1
fi

# Testing Python version

VERSION="$( $PYTHON_CMD --version)"
MAJOR="$(echo $VERSION |cut -d' ' -f2 | cut -d'.' -f1)"

if [[ $MAJOR -lt 2 ]]; then
   echo
   echo Python3 is required, please install it and relaunch this script >&2
   exit 1
fi

MINOR="$( echo $VERSION | cut -d' ' -f2 | cut -d'.' -f 2 )"

if [[ $MINOR -lt 5 ]]; then
   echo
   echo "Using python version lower than 3.5 hasn't been tested" >&2
   echo "you'd better use python > 3.5" >&2
fi

if ! $PYTHON_CMD -c "import PyQt5" >/dev/null 2>&1; then
   echo
   echo Cant find PyQt5, please install it and rerun this script >&2
   exit 1
fi

# Starting PSP Python Gui

echo Starting py_launcher

cd GUI && $PYTHON_CMD py_GUI_launcher.py

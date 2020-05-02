#!/bin/bash

ROOTDIR=$(realpath $(dirname $(realpath "$0"))/..)
FILES="$(find ${ROOTDIR}/python3 -name '*.py' | tr '\n' ' ')"
autopep8 -ia --ignore=E402,E501 ${FILES}

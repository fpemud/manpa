#!/bin/bash

FILES="python3/manpa.py"
autopep8 -ia --ignore=E402,E501 ${FILES}

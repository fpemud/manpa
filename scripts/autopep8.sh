#!/bin/bash

FILES="python3/*.py"
autopep8 -ia --ignore=E402,E501 ${FILES}

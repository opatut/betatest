#!/bin/bash

if [[ $VIRTUAL_ENV == "" ]]; then
    source env/bin/activate
fi

python betatest.py

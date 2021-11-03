#!/bin/bash

if [ -d "gen_creds.sh" ]; then
    echo "*** skipping credentials ***"
else
    echo "*** populating credentials ***"
    sh gen_creds.sh
fi

if [ -d "venv" ]; then
    if [ $OSTYPE = msys ]; then
        . ./venv/Scripts/activate
    else
        . ./venv/bin/activate
    fi
else
    echo "*** setting up virtual env ***"
    python3.7 -m venv venv
    if [ $OSTYPE = msys ]; then
        . ./venv/Scripts/activate
        pip install -r requirements.txt
    else
        . ./venv/bin/activate
        pip install -r requirements.txt
    fi
fi

nohup python src/scheduler.py &
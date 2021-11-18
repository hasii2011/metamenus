#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

# cd src > /dev/null 2>&1
echo "current: `pwd`"

mypy --config-file .mypi.ini --show-error-codes --no-color-output --exclude locale metamenus demo tests
status=$?

echo "Exit with status: ${status}"
exit ${status}


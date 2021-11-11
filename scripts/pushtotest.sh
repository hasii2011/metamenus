#!/bin/bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}
changeToProjectRoot

clear

twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*

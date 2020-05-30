#!/bin/bash

# move to project root folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" 
cd "${DIR}/../"

if [ -z "$FLASKELETON_CONFIG" ];
then
    export FLASKELETON_CONFIG=./config.yml
fi

if [ "$#" -lt 1 ];
then
    echo 'No environment provided.'
    exit 1
fi

test_env=$(echo 'dev prod' | grep -Fw "$1")
if [ -z "${test_env}" ];
then
    echo 'Unknown environment.'
    exit 1
fi
export FLASKELETON_ENV="$1"
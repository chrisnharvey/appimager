#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $OWD

eval "${DIR}/python3 ${DIR}/../../appimager/appimager" "$@"

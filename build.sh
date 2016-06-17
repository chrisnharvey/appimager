#!/bin/bash

cmake .
make clean
make

mv ./runtime build/runtime

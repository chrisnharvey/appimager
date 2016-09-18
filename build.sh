#!/bin/bash

cd /mnt/appimager/work

wget -O /mnt/appimager/work/virtualenv.tar.gz https://pypi.python.org/packages/8b/2c/c0d3e47709d0458816167002e1aa3d64d03bdeb2a9d57c5bd18448fd24cd/virtualenv-15.0.3.tar.gz#md5=a5a061ad8a37d973d27eb197d05d99bf
tar xf /mnt/appimager/work/virtualenv.tar.gz
cd virtualenv*
python3.5 setup.py install

virtualenv /mnt/appimager/build

/mnt/appimager/build/bin/pip3 install -r /mnt/appimager/cwd/requirements.txt

mkdir /mnt/appimager/build/appimager
cp -R /mnt/appimager/cwd/core /mnt/appimager/build/appimager
cp -R /mnt/appimager/cwd/cli /mnt/appimager/build/appimager
cp /mnt/appimager/cwd/appimager /mnt/appimager/build/appimager/appimager

cp /mnt/appimager/cwd/AppImager.sh /mnt/appimager/build/bin/AppImager.sh
cp /mnt/appimager/cwd/Icon.png /mnt/appimager/build/Icon.png
cp /mnt/appimager/cwd/AppImager.desktop /mnt/appimager/build/AppImager.desktop

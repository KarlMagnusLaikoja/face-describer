#!/usr/bin/env bash
apt-get install python3-pip;
pip3 install virtualenv;
virtualenv venv;
source venv/bin/activate;

#Install cmake, dlib, face-recognition separately to guarantee correct order
pip install cmake==3.27.7;
pip install dlib==19.24.2;
pip install face-recognition==1.3.0;

#Install the other requirements from text file
pip install -r requirements.txt

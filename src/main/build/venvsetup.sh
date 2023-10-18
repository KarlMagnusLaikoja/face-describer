#!/usr/bin/env bash
sudo apt-get install python3-pip;
sudo pip install virtualenv;
virtualenv venv;
source venv/bin/activate;


sudo python3 conda install -c conda-forge dlib;
sudo pip install cmake;
sudo pip install face_recognition;
sudo pip install opencv-python;

#!/usr/bin/env bash
sudo apt-get install python3-pip;
sudo pip3 install virtualenv;
virtualenv venv;
source venv/bin/activate;


sudo pip install -r requirements.txt

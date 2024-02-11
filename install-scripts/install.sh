#!/bin/bash
sudo sudo apt-get update -y && sudo apt-get install python3-pip zip -y
pip3 install -r requirements.txt

#git config --global user.name "Xabi Ezpeleta"
#git config --global user.email xezpleta@gmail.com

bash ./versions.sh

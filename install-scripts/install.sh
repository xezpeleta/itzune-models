#!/bin/bash
sudo sudo apt-get update -y && sudo apt-get install python3-pip zip -y

if [ ! -d ".venv" ]; then
	python3 -m venv .venv
fi
source .venv/bin/activate

pip3 install -r requirements.txt

#git config --global user.name "Xabi Ezpeleta"
#git config --global user.email xezpleta@gmail.com

bash ./versions.sh

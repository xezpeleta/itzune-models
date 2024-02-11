.PHONY: install get-corpus train-eng-cat

install:
	cd install-scripts && ./install.sh

get-corpus:
	cd languages && ./get-corpuses.sh

trian-en-eu:
	cd languages/en-eu/ && ./voc.sh && ./train.sh

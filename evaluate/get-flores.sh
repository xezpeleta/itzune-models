#!/bin/bash

# The data is only available in this format in order to avoid it being picked up by crawlers, which would lead to it being accidentally included in the sort of web corpora often used to train LLMs and large scale machine translation models, rendering it useless as a benchmark.

wget -O flores.zip https://github.com/openlanguagedata/flores/releases/download/v2.0-alpha.2/floresp-v2.0-alpha.2.zip
unzip -P "multilingual machine translation" flores.zip
cp flores/dev/dev.eus_Latn flores200.eus
cp flores/dev/dev.eng_Latn flores200.eng
cp flores/dev/dev.spa_Latn flores200.spa
cp flores/dev/dev.fra_Latn flores200.fra

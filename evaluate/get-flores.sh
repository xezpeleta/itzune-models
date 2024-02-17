#!/bin/bash

# The data is only available in this format in order to avoid it being picked up by crawlers, which would lead to it being accidentally included in the sort of web corpora often used to train LLMs and large scale machine translation models, rendering it useless as a benchmark.

wget -O flores.zip https://github.com/openlanguagedata/flores/releases/download/v2.0-alpha.2/floresp-v2.0-alpha.2.zip
unzip -P "multilingual machine translation" flores.zip
cp floresp-v2.0-alpha.2/devtest/devtest.eus_Latn flores200.eus
cp floresp-v2.0-alpha.2/devtest/devtest.eng_Latn flores200.eng
cp floresp-v2.0-alpha.2/devtest/devtest.spa_Latn flores200.spa
cp floresp-v2.0-alpha.2/devtest/devtest.fra_Latn flores200.fra

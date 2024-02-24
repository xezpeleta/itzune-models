# Introduction

This repository contains the scripts to train neuronal translation models for [OpenNMT](https://opennmt.net/) and also the Itzune published models.

This repository has been created based on the work of [Softcatalà](https://www.softcatala.org/). We have adapted the scripts and corpus to train models for the Basque language.

The corpus used to train these models are available here: https://huggingface.co/datasets/itzune/basque-parallel-corpus

And here the tools to serve these models in production: https://github.com/xezpeleta/itzune-models

# Models
Language pair | Itzune BLEU | Itzune Flores200 BLEU | Google BLEU | Meta NLLB200 BLEU | Opus-MT BLEU | Sentences | Download model
|---|---|---|---|---|---|---|---
|English-Basque | 26.6 |17.6 |- |13.2|11.3| 19050400 | [eng-eus-2024-02-20.zip](https://huggingface.co/itzune/itzune-models-zip/raw/main/eng-eus-2024-02-20.zip)

Legend:
* *SC Model BLEU* column indicates the Itzune models' BLEU score against the corpus test dataset (from train/dev/test)
* *SC Flores200 BLEU* column indicates the Itzune models' BLEU score against [Flores200 benchmark dataset](https://github.com/facebookresearch/flores). This provides an external evaluation
* *Google BLEU* is the BLUE score of Google Translate using the Flores200 benchmark
* *Opus-MT BLEU* is the BLUE score of the [Opus-MT models](https://github.com/Helsinki-NLP/Opus-MT) using the Flores200 benchmark (our ambition is to outperform them)
* *Sentences* is the number of sentences in the corpus used for training
* Meta NLLB200 refers to nllb-200-3.3B model from Meta. This is a very slow model and it's distilled version performs significantly worse.

Notes:
* All models are based on TransformerRelative and SentencePiece has been used as tokenizer.
* We use [Sacrebleu](https://github.com/mjpost/sacrebleu) to calculate BLUE scores with the 13a tokenizer.
* These models are used in production with modest hardware (CPU). As result, these models are a balance between precision and latency. It is possible to further improve BLUE scores by ~+1 BLEU, but at a significant latency cost at inference.
* BLEU is the most popular metric for evaluating machine translation but also broadly acknowledged that it is not perfect. It's estimated that has a [~80% correlation](https://aclanthology.org/W05-0909.pdf) with human judgment
* Flores200 has some limitations. It was produced translating from English to many of the other languages.

## Structure of the models

Description of the directories on the contained in the models zip file:

* *tensorflow*: model exported in Tensorflow format
* *ctranslate2*: model exported in CTranslate2 format (used for inference)
* *metadata*: description of the model
* *tokenizer*: SentencePiece models for both languages

# Using the models

You can use the models with https://github.com/OpenNMT/CTranslate2 which offers fast inference.


Download the model and unpack it:

```bash
wget https://huggingface.co/itzune/itzune-models-zip/raw/main/eng-eus-2024-02-14.zip
unzip eng-eus-2024-02-14.zip
```

Install dependencies:

```pip3 install ctranslate2 pyonmttok```

Simple translation using Python:

```python

import ctranslate2
translator = ctranslate2.Translator("eng-eus/ctranslate2/")
translator.translate_batch([["▁Hello", "▁world", "!"]])
[[{'tokens': ['▁Kaixo', '▁mundua', '!']}]]

```

Simple tokenization & translation using Python:


```python
import pyonmttok
import ctranslate2

tokenizer=pyonmttok.Tokenizer(mode="none", sp_model_path = "eng-eus/tokenizer/sp_m.model")
tokenized=tokenizer.tokenize("Hi this is a test")

translator = ctranslate2.Translator("eng-eus/ctranslate2/")
results = translator.translate_batch([tokenized[0]])

print(tokenizer.detokenize(results[0].hypotheses[0]))
# Output: Kaixo hau proba bat da
```
# Training the models

In order to train models you should have a GPU.

## Training in a machine

First you need to install the necessary packages:

```shell

make install
```

After this, you download be all the corpuses:


```shell

make get-corpus
```

To train the English - Basque model type:

```shell

make train-eng-eus
```



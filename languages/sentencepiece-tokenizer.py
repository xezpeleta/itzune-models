#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import pyonmttok
import os
from optparse import OptionParser

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-v',
        '--vocabulary-size',
        type='int',
        action='store',
        default='32000',
        dest='vocabulary_size',
        help='Size of the vocabulary'
    )

    parser.add_option(
        '-c',
        '--create_model',
        action='store_true',
        default='False',
        dest='create_model',
        help='Create tokenizer model'
    )

    (options, args) = parser.parse_args()
    return options.vocabulary_size, options.create_model

def _get_file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def ingest_file(learner, ingest_file):
    MAX_LINES = 1000000

    file_len = _get_file_len(ingest_file)

    if file_len < MAX_LINES:
        return learner.ingest_file(ingest_file)

    percentage = MAX_LINES / file_len * 100
    print(f"Ingesting only {percentage:.2f}% of {ingest_file}")

    cnt = 0
    reduced_file = ingest_file + "-reduced.txt"
    with open(ingest_file, "r") as source,\
         open(reduced_file, "w") as target:

        while True:
            src = source.readline()
            if not src:
                break

            cnt = cnt + 1

            if cnt > 100:
                cnt = 0

            if cnt > percentage:
                continue

            target.write(src)

    learner.ingest_file(reduced_file)
    return reduced_file
    
def create_model(vocabulary_size, model_name):
    learner = pyonmttok.SentencePieceLearner(vocab_size=vocabulary_size,
                                             keep_vocab=True)
    reduced_src = ingest_file(learner, "src-train.txt")
    reduced_tgt = ingest_file(learner, "tgt-train.txt")
    tokenizer = learner.learn(model_name, verbose=True)

    os.remove(reduced_src)
    os.remove(reduced_tgt)
    return tokenizer

def tokenize_files(tokenizer):

    tokens = tokenizer.tokenize_file("src-train.txt", "src-train.txt.token")
    tokens = tokenizer.tokenize_file("src-val.txt", "src-val.txt.token")

    tokens = tokenizer.tokenize_file("tgt-train.txt", "tgt-train.txt.token")
    tokens = tokenizer.tokenize_file("tgt-val.txt", "tgt-val.txt.token")


def main():

    print("Creates tokenized output corpus using SentencePiece")
    vocabulary_size, _create_model = read_parameters()
    model_name = 'sp_m'
    if _create_model is True:
        print("Vocabulary size {0}".format(vocabulary_size))
        tokenizer = create_model(vocabulary_size, model_name)
    else:
        tokenizer = pyonmttok.Tokenizer(mode="none", sp_model_path = f"{model_name}.model")

    tokenize_files(tokenizer)

if __name__ == "__main__":
    main()

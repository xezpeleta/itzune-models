#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WAR   RANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import datetime
import json
import urllib
import urllib.request
import itzuli
import time
from optparse import OptionParser

def file_len(fname):
    if not os.path.isfile(fname):
        return 0

    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass

    return i + 1

def get_sacrebleu(reference_file, hypotesis_file ,target_language):
    JSON_FILE = 'bleu.json'
    
    if target_language == "jpn":
        tokenizer="--tokenize ja-mecab"
    else:
        tokenizer = ""

    cmd = f'sacrebleu {tokenizer} {reference_file}  -i {hypotesis_file} -m bleu > {JSON_FILE}'
    os.system(cmd)
    with open(JSON_FILE) as f:
        data = json.load(f)

    return f"{data['score']:0.1f}"

def save_json(scores):
	with open("elia-bleu.json", "w") as outfile:
		json.dump(scores, outfile, indent=4)


def _translate_text_elia(text, pair):
    
    src_lang, tgt_lang = pair.split("-")
    translated = itzuli.translate(text, src_lang, tgt_lang)
    # Respect eizu.eus - wait 30 seconds
    time.sleep(30)
    return translated


def translate_elia(source, target, pair):

    strings = 0
    with open(source, 'r') as tf_en, open(target, 'w') as tf_ca:
        en_strings = tf_en.readlines()

        cnt = 0
        for string in en_strings:
            cnt = cnt + 1
    
            try:
                translated = _translate_text_elia(string, pair)
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

            except Exception as e:
                print(e)
                print(string)

                translated = 'Error'
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

    print("Translated {0} strings".format(strings))
    
    
    

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-k',
        '--key',
        action='store',
        type='string',
        dest='key',
        default='',
        help='API Key to use (if applies)'
    )

    (options, args) = parser.parse_args()

    return options.key




def main():
    print("Translates flores200 datasets using Elhuyar Elia.eus")
    
    pair_languages = {
        "en-eu" : ["eng", "eus"],
        "eu-en" : ["eus", "eng"],
    }

    blue_scores = {}
    for pair_language in pair_languages:
        source_language = pair_languages[pair_language][0]
        target_language = pair_languages[pair_language][1]
#        print(f"source_language: {source_language}")
#        print(f"target_language: {target_language}")

        hypotesis_file = f"elia-translate/flores200-{source_language}-{target_language}.{target_language}"
        input_file = f"flores200.{source_language}"

        print(f"hypo {hypotesis_file}")
        print(f"input_file {input_file}")

        start_time = datetime.datetime.now()
        LINES_IN_DATA_SET = 1012
        if file_len(hypotesis_file) != LINES_IN_DATA_SET:
            translate_elia(input_file, hypotesis_file, f"{pair_language}")
            

        reference_file = f"flores200.{target_language}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file, target_language)
        blue_scores[f'{source_language}-{target_language}'] = sacrebleu
        print(f"'{source_language}-{target_language}', BLEU: '{sacrebleu}'")
    save_json(blue_scores)
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)

if __name__ == "__main__":
    main()

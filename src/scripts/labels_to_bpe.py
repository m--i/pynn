#!/usr/bin/env python3

# Copyright 2020 Maximilian Awiszus
# Licensed under the Apache License, Version 2.0 (the "License")

import argparse
import sentencepiece as spm

from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description='Conver an audio file to wav in parallel.')
parser.add_argument('--vocabulary', help='path to vocabulary text file', type=str, default=None)
parser.add_argument('--model', help='path to already trained BPE model', type=str, default=None)
parser.add_argument('--label', help='path to label file', type=int, default=1)
parser.add_argument('--out', help='path to output file', type=int, default='tr-label.bpe')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.voabulary is not None:
        spm.SentencePieceTrainer.train(input=args.vocabulary, model_prefix='m', vocab_size=32000, character_coverage=0.9995, model_type='bpe', bos_id=-1, eos_id=-1)
    elif args.model is not None:
        sp = spm.SentencePieceProcessor(model_file=args.model)
        with open(args.label, 'r') as label_file:
            with open(args.out, 'w') as bpe_file:
                for label in label_file:
                    bpe_file.write(' '.join([str(i) for i in sp.encode(label)]))


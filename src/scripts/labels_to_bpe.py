#!/usr/bin/env python3

# Copyright 2020 Maximilian Awiszus
# Licensed under the Apache License, Version 2.0 (the "License")

import argparse
import sentencepiece as spm

from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description='Convert an audio file to wav in parallel.')
parser.add_argument('--vocabulary', help='path to vocabulary text file', type=str, default=None)
parser.add_argument('--model', help='path to already trained BPE model', type=str, default=None)
parser.add_argument('--label', help='path to label file', type=str)
parser.add_argument('--out', help='path to output file', type=str, default='tr-label.bpe')

MODEL_PREFIX = 'bpe'

if __name__ == '__main__':
    args = parser.parse_args()
    if args.vocabulary is not None:
        spm.SentencePieceTrainer.train(input=args.vocabulary, model_prefix=MODEL_PREFIX, vocab_size=4000, character_coverage=1.0, model_type='bpe', bos_id=-1, eos_id=-1)
        with open(MODEL_PREFIX + '.vocab', 'r') as bpe_vocab_file:
            with open(MODEL_PREFIX + '.dict', 'w') as bpe_dict_file:
                for i, line in enumerate(bpe_vocab_file):
                    token = line.split()[0]
                    bpe_dict_file.write('{} {}\n'.format(token, i))
    elif args.model is not None:
        sp = spm.SentencePieceProcessor(model_file=args.model)
        with open(args.label, 'r') as label_file:
            with open(args.out, 'w') as bpe_file:
                for label in label_file:
                    bpe_file.write(' '.join([str(i) for i in sp.encode(label)]) + '\n')


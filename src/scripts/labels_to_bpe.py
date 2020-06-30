#!/usr/bin/env python3

# Copyright 2020 Maximilian Awiszus
# Licensed under the Apache License, Version 2.0 (the "License")

import argparse
import sentencepiece as spm

from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description='Convert an audio file to wav in parallel.')
parser.add_argument('--sentences', help='path to sentences file', type=str, default=None)
parser.add_argument('--model', help='path to already trained bpe model', type=str, default=None)
parser.add_argument('--label', help='path to label file', type=str, default='train_cleaned.txt')
parser.add_argument('--out', help='path to output file', type=str, default='tr-label.bpe')
parser.add_argument('--vocab-size', help='size of vocabulary', type=int, default=40000)
parser.add_argument('--character-coverage', help='coverage for characters', type=float, default=0.9995)

MODEL_PREFIX = 'bpe'

if __name__ == '__main__':
    args = parser.parse_args()
    if args.sentences is not None:
        spm.SentencePieceTrainer.train(input=args.sentences, model_prefix=MODEL_PREFIX, vocab_size=args.vocab_size, character_coverage=args.character_coverage, model_type='bpe', bos_id=-1, eos_id=-1)
        print('Saving dict: {}.dict'.format(MODEL_PREFIX))
        with open(MODEL_PREFIX + '.vocab', 'r') as bpe_vocab_file:
            with open(MODEL_PREFIX + '.dict', 'w') as bpe_dict_file:
                for i, line in enumerate(bpe_vocab_file):
                    token = line.split()[0]
                    bpe_dict_file.write('{} {}\n'.format(token, i))
    elif None not in [args.model, args.label, args.out]:
        sp = spm.SentencePieceProcessor(model_file=args.model)
        with open(args.label, 'r') as label_file:
            with open(args.out, 'w') as bpe_file:
                for line in label_file:
                    utt, sent = line.split(maxsplit=1)
                    sent = sent.replace('\n','')
                    encoding = sp.encode(sent)
                    # ToDo: something wrong with sentencepiece here?
                    #if encoding[0] == 3:
                    #    encoding = encoding[1:]
                    bpe_file.write(utt + ' ' + ' '.join([str(id) for id in encoding]) + '\n')


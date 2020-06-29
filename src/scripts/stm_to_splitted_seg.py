#!/usr/bin/env python3

# Copyright 2020 Maximilian Awiszus
# Licensed under the Apache License, Version 2.0 (the "License")

import argparse
import os
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description='Make a train, validation test subset split for a dataset.')
parser.add_argument('--src-file', help='path to stm or scp file', type=str, required=True)
parser.add_argument('--train-size', help='size of train subset', type=float, default=0.65)
parser.add_argument('--train', help='name of train subset', type=str, default="tr")
parser.add_argument('--validation-size', help='size of validation subset', type=float, default=0.15)
parser.add_argument('--validation', help='name of validation subset', type=str, default="vl")
parser.add_argument('--test-size', help='size of test subset', type=float, default=0.2)
parser.add_argument('--test', help='name of test subset', type=str, default="ts")

if __name__ == '__main__':
    args = parser.parse_args()

    assert args.train_size + args.validation_size + args.test_size == 1.0

    scr_filename, src_suffix = os.path.splitext(args.src_file)
    with open(args.src_file, 'r') as src_file:
        segs = []
        for stm_line in src_file:
            if src_suffix == '.stm':
                if stm_line[0] != ';':
                    utt, chnl, spk, start, dur, meta, sent = stm_line.split(maxsplit=6)
                    segs.append('{}\t{}\t{}\t'.format(utt, start, dur))
            elif src_suffix == '.scp':
                segs.append(stm_line.replace('\n', ''))
            else:
                print("Error type of 'src-file' is not supported.")
        train_val_subset, test_subset, _, _ = train_test_split(segs, range(len(segs)), test_size=args.test_size)
        val_size = args.validation_size / (1.0 - args.test_size)
        train_subset, val_subset, _, _ = train_test_split(train_val_subset, range(len(train_val_subset)), test_size=val_size)
    
    suffix = '.seg'
    if src_suffix == '.scp':
        suffix = '.scp'
    with open(scr_filename + '-' + args.train + suffix, 'w') as seg_file:
        seg_file.write('\n'.join(train_subset))

    with open(scr_filename + '-' + args.validation + suffix, 'w') as seg_file:
        seg_file.write('\n'.join(val_subset))
    
    with open(scr_filename + '-' + args.test + suffix, 'w') as seg_file:
        seg_file.write('\n'.join(test_subset))

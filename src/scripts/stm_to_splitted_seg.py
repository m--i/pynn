#!/usr/bin/env python3

# Copyright 2020 Maximilian Awiszus
# Licensed under the Apache License, Version 2.0 (the "License")

import argparse
import os
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description='Make a train, validation test subset split for a dataset.')
parser.add_argument('--stm-file', help='path to scp file', type=str, required=True)
parser.add_argument('--sync-scp-file', help='path to scp file', type=str, default=None)
parser.add_argument('--train-size', help='size of train subset', type=float, default=0.65)
parser.add_argument('--train', help='name of train subset', type=str, default="tr")
parser.add_argument('--validation-size', help='size of validation subset', type=float, default=0.15)
parser.add_argument('--validation', help='name of validation subset', type=str, default="vl")
parser.add_argument('--test-size', help='size of test subset', type=float, default=0.2)
parser.add_argument('--test', help='name of test subset', type=str, default="ts")
parser.add_argument('--export-segs', help='export seg file (utt, start, duration)', action='store_true')
parser.add_argument('--export-lbls', help='export label file (utt, sentence)', action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()

    assert args.train_size + args.validation_size + args.test_size == 1.0

    scr_filename, src_suffix = os.path.splitext(args.stm_file)
    utts = []
    stms = {}
    segs = {}
    scps = {}
    lbls = {}
    with open(args.stm_file, 'r') as stm_file:
        for stm_line in stm_file:
            if stm_line[0] != ';':
                utt, chnl, spk, start, dur, meta, sent = stm_line.split(maxsplit=6)
                utts.append(utt)
                stms[utt] = stm_line.replace('\n', '')
                if args.export_segs:
                    segs[utt] = '{}\t{}\t{}'.format(utt, start, dur)
                if args.export_lbls:
                    lbls[utt] = '{} {}'.format(utt, sent.replace('\n', '').replace(' ','').strip())
        train_val_subset, test_subset, _, _ = train_test_split(utts, range(len(utts)), test_size=args.test_size)
        val_size = args.validation_size / (1.0 - args.test_size)
        train_subset, val_subset, _, _ = train_test_split(train_val_subset, range(len(train_val_subset)), test_size=val_size)

    if not args.sync_scp_file is None:
        with open(args.sync_scp_file, 'r') as scp_file:
            for scp_line in scp_file:
                utt, ptr = scp_line.split(maxsplit=1)
                utt = utt.replace('.flac.wav', '')
                scps[utt] = '{} {}'.format(utt, ptr.replace('\n', ''))

    for utts, suffix in zip([train_subset, val_subset, test_subset], [args.train, args.validation, args.test]):
        with open('{}-{}.stm'.format(scr_filename, suffix), 'w') as stm_file:
            stm_file.write('\n'.join([stms[utt] for utt in utts]))
        if args.export_segs:
            with open('{}-{}.seg'.format(scr_filename, suffix), 'w') as seg_file:
                seg_file.write('\n'.join([segs[utt] for utt in utts]))
        if args.export_lbls:
            with open('{}-{}.txt'.format(scr_filename, suffix), 'w') as lbl_file:
                lbl_file.write('\n'.join([lbls[utt] for utt in utts]))
        if not args.sync_scp_file is None:
            with open('{}-{}.scp'.format(scr_filename, suffix), 'w') as scp_file:
                scp_file.write('\n'.join([scps[utt] for utt in utts]))

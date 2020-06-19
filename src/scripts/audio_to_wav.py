#!/usr/bin/env python3

# Copyright 2020 Maximilian Awiszus
# Licensed under the Apache License, Version 2.0 (the "License")

import argparse
import multiprocessing

from os import listdir
from os.path import isfile, join
from subprocess import call

def write_ark_thread(audio_files, args):
    for audio_file in audio_files:
        audio_file_path = join(args.audio_path, audio_file)
        print('Processing {}…'.format(audio_file))
        call('sox "{}" -r 16000 -c 1 -b 16 -e signed "{}.wav" -q'.format(audio_file_path, audio_file_path), shell=True)

parser = argparse.ArgumentParser(description='pynn')
parser.add_argument('--audio-path', help='path to audio files', type=str, default=None)
parser.add_argument('--jobs', help='number of parallel jobs', type=int, default=1)

if __name__ == '__main__':
    args = parser.parse_args()
    audio_files = [f for f in listdir(args.audio_path) if isfile(join(args.audio_path, f)) and f.endswith('.flac')]
    size = len(audio_files) // args.jobs
    jobs = []
    j = 0
    for i in range(args.jobs):
        l = len(audio_files) if i == (args.jobs-1) else j+size
        sub_audio_files = audio_files[j:l]
        j += size
         
        process = multiprocessing.Process(
                target=write_ark_thread, args=(sub_audio_files, args))
        process.start()
        jobs.append(process)
    
    for job in jobs: job.join()
    

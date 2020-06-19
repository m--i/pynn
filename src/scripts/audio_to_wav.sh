#!/bin/bash
data_dir=/media/maximilian/Elements/Datasets/open_voice_de/clips

# Convert audio to 16khz -> wavs/*.wav
for i in $data_dir/*.mp3; do
    sox "$i" -r 16000 -c 1 -b 16 -e signed "${i%.mp3}.wav" -q
done


# Issues?
# - sox FAIL formats: no handler for file extension `mp3':
# sudo apt-get install libsox-fmt-mp3
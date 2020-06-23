#!/bin/bash
data_dir=/project/OML/mawiszus/data/common_voice_de

working_dir=`pwd`

pynndir=/home/mawiszus/projects/pynn/src  # pointer to pynn
device=gpu0  # the device to be used. set it to "cpu" if you don't have GPUs

# export environment variables
export PATH="/usr/local/cuda/bin/:$PATH"
export PYTHONPATH=$pynndir
export CUDA_DEVICE_ORDER=PCI_BUS_ID

pythonCMD="python -u -W ignore"

mkdir -p model

CUDA_VISIBLE_DEVICES=1 $pythonCMD $pynndir/pynn/bin/train_seq2seq.py \
                                  --train-scp $data_dir/test.scp --train-target $data_dir/tr-label.bpe --spec-drop --time-stretch --fp16 \
                                  --valid-scp $data_dir/test.scp --valid-target $data_dir/cv-label.bpe --use-cnn --freq-kn 3 --freq-std 2 \
                                  --n-classes 8003 --d-input 40 --d-model 1024 --downsample 1 --n-enc 6 --n-dec 2 --shared-emb \
                                  --dropout 0.35 --emb-drop 0.35 --lr 4.0 --b-input 32000 --b-update 6000 --n-warmup 8000 --shuffle --grad-norm 2>&1 | tee run-seq2seq.log

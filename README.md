# pynn

## Requirements
To install the (cpu) requirements conda is used in this project rogether with Python3. For more information about Conda see https://docs.conda.io/en/latest/miniconda.html

Create the `pynn` conda ennvironment with the following command:
```
conda env create -f environment.yml
conda activate web
```

## Feature extraction
For the feature extraction [wav_to_fbank.py](src/pynn/bin/wav_to_fbank.py) can be used.
The reqired argument is the `--seg-desc` which contains the path to a segment description file. The format should be

|audio | start time | end time |
| ---- | ---------- | -------- |
| utt_0000051685-usr_0006 | 1.56 | 8.29|

Combine all extracted scp file with

```
cat data.*.scp > data.scp
```
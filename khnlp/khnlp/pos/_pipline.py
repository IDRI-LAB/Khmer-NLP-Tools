import warnings

from khnlp.logger import write_log

warnings.filterwarnings('ignore')

from khnlp.pos.util import sent2features
from khnlp.util import data
import khnlp.crf as crf

import re


def _preprocess(sent):
    sent = sent.strip()
    sent = re.sub(r'\u200b', '', sent)
    sent = re.sub(r'\s+', ' ', sent)

    X = []
    y = []
    for i in range(0, len(sent.split())):
        parts = sent[i].split('/')
        token = parts[0]
        label = parts[1]

        X.append(token)
        y.append(label)

    return X, y


def _load_data(files: [str]):
    dataset = data.load_simple_data(files, _preprocess)
    X, y = zip(*dataset)
    return X, y


def _data2features(data):
    return sent2features(data)


@write_log(path='{output_dir}/log.txt')
def train(train_files, test_files, output_dir, load_data=None, data2features=None, **kwargs):
    if load_data is None:
        load_data = _load_data
    if data2features is None:
        data2features = _data2features

    crf.train(train_files=train_files, test_files=test_files, output_dir=output_dir, load_data=load_data,
              data2features=data2features, **kwargs)


@write_log(path='{output_dir}/log.txt')
def test(model_file, test_files, output_dir, load_data=None, data2features=None):
    if load_data is None:
        load_data = _load_data
    if data2features is None:
        data2features = _data2features

    crf.test(model_file=model_file, test_files=test_files, output_dir=output_dir, load_data=load_data,
             data2features=data2features)

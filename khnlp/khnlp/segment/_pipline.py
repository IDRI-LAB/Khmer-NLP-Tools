import warnings

from khnlp.logger import write_log

warnings.filterwarnings('ignore')

from khnlp.segment import get_char_type, sent2features, export_vocab
from khnlp.util.data import load_simple_data
import khnlp.crf as crf

import re


def _preprocess(sent):
    sent = sent.strip()
    sent = re.sub(r'\u200b', '', sent)
    sent = re.sub(r'\s+', ' ', sent)

    X = []
    y = []
    for i in range(0, len(sent)):
        char = sent[i]
        prev_char = sent[i - 1] if i > 1 else ''
        next_char = sent[i + 1] if i < len(sent) - 1 else ''

        if char.isspace():
            continue

        type_ = get_char_type(prev_char, char, next_char)
        label = '1' if next_char == ' ' else '0'

        X.append((char, type_))
        y.append(label)

    return X, y


def _load_data(files: [str]):
    dataset = load_simple_data(files, _preprocess)
    X, y = zip(*dataset)
    return X, y


def _data2features(data):
    return sent2features(data)


@write_log(path='{output_dir}/log.txt')
def test(model_file, test_files, output_dir, load_data=_load_data, data2features=_data2features):
    crf.test(model_file=model_file, test_files=test_files, output_dir=output_dir, load_data=load_data,
             data2features=data2features)

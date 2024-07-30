import warnings

from khnlp.logger import write_log

warnings.filterwarnings('ignore')

import khnlp.romanize.util as util
import khnlp.crf as crf


def _load_data(files: [str]):
    return util.load_data(files)


def _data2features(data):
    return util.name2features(data)

@write_log(path='{output_dir}/log.txt')
def test(model_file, test_files, output_dir, load_data=None, data2features=None):
    if load_data is None:
        load_data = _load_data
    if data2features is None:
        data2features = _data2features

    crf.test(model_file=model_file, test_files=test_files, output_dir=output_dir, load_data=load_data,
             data2features=data2features)

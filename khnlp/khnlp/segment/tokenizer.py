import pickle
import re

from khnlp.segment import get_char_type, sent2features, UNKNOWN, ZERO_WIDTH_SPACE, NUMBER


class Tokenizer(object):

    def __init__(self, model_file: str, preprocess=lambda x: x, postprocess=lambda x: x):
        self.preprocess_ = preprocess
        self.postprocess_ = postprocess
        self.model = pickle.load(open(model_file, 'rb'))

    def preprocess(self, sent):
        sent = sent.strip()

        # separate khmer chars from other
        sent = re.sub(r'([ក-៹])([^.,ក-៹])', r'\1 \2', sent)
        sent = re.sub(r'([^.,ក-៹])([ក-៹])', r'\1 \2', sent)

        sent = re.sub(r'\u200b', '', sent)
        sent = re.sub(r'\s+', ' ', sent)
        sent = re.sub(r'\s', '\u200b', sent)
        
        # additional preprocessing
        sent = self.preprocess_(sent)

        # prepare input
        sample = []
        for i in range(0, len(sent)):
            char = sent[i]
            prev_char = sent[i - 1] if i > 0 else ''
            next_char = sent[i + 1] if i < len(sent) - 1 else ''

            char_type = get_char_type(prev_char, char, next_char)
            sample.append((char, char_type, None))

        return sample

    def postprocess(self, sent):
        sent = sent.strip()
        sent = re.sub(r'\u200b', ' ', sent)
        sent = re.sub(r'\s+', ' ', sent)
        
        # additional postprocessing
        sent = self.postprocess_(sent)
        
        return sent

    def tokenize(self, sents):
        if type(sents) == str:
            sents = [sents]

        sents = [self.preprocess(s) for s in sents]

        labels = self.model.predict([sent2features(s) for s in sents])

        results = []
        for sent_, label_ in zip(sents, labels):
            result = ''

            for i in range(0, len(sent_)):
                char = sent_[i][0]
                char_type = sent_[i][1]
                next_char_type = sent_[i + 1][1] if i < len(sent_) - 1 else UNKNOWN[1]
                label = label_[i]

                if char_type == ZERO_WIDTH_SPACE[1]:
                    result += ' '
                else:
                    result += char
                    if char_type == NUMBER[1]:
                        # NS char
                        if next_char_type != NUMBER[1]:
                            result += ' '
                    elif label == '1':
                        result += ' '

            result = self.postprocess(result)
            results.append(result)

        return results if len(results) > 1 else results[0]

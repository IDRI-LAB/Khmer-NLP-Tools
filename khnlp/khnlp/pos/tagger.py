import pickle
import re

import khnlp.pos.util as util


class PoSTagger(object):

    def __init__(self, model_file: str):
        self.model = pickle.load(open(model_file, 'rb'))

    def preprocess(self, sent):
        sent = sent.strip()
        sent = re.sub(r'\u200b', '', sent)
        sent = re.sub(r'\s+', ' ', sent)
        
        tokens = sent.split()
        return tokens

    def tag(self, sents):
        if type(sents) == str:
            sents = [sents]

        sents = [self.preprocess(s) for s in sents]

        labels = self.model.predict([util.sent2features(s) for s in sents])

        results = []
        for sent_, label_ in zip(sents, labels):
            result = []

            for sent in sent_:
                token = sent[0]
                label = sent[1]
                result = result.append((token, label))

            results.append(result)

        return results if len(results) > 1 else results[0]

import pickle

from khnlp.romanize.util import name2features


class Romanizer(object):

    def __init__(self, model_file: str):
        self.model = pickle.load(open(model_file, 'rb'))

    def preprocess(self, name):
        sample = []
        for idx, char in enumerate(name):
            if char == ' ':
                sample.append('_')
                continue

            sample.append(char)

            next_char = name[idx + 1] if idx < len(name) - 1 else char
            if 6016 <= ord(char) <= 6050:
                if 6016 <= ord(next_char) <= 6050 or next_char == ' ':
                    sample.append('@')

        return name2features(sample)
    
    def postprocess(self, name):
        result = ''
        for char in name:
            if char == '@':
                continue
            elif char == '_':
                result += ' '
            else:
                result += char
        return result

    def romanize(self, names):
        if type(names) == str:
            names = [names]
        
        names = [self.preprocess(n) for n in names]
        
        latins = self.model.predict(names)

        latins = [self.postprocess(n) for n in latins]

        return latins if len(latins) > 1 else latins[0]

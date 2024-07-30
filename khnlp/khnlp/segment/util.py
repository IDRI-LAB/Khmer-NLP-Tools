import re
from collections import Counter

from tqdm import tqdm

CONSONANT           = ('[ក-អ]', 'C')
VOWEL               = ('[ា-ៈ]', 'V')
IND_VOWEL           = ('[ឤឥឦឧឩឳឰឬឫឭឮឯឱឲឪ]', 'IV')
UPPER_SIGN          = ('[៉-៑]', 'US')
ATAK_NUMBER         = ('[៰-៹]', 'AN')
LUNAR_NUMBER        = ('[᧠-᧿]', 'LN')
SUBSCRIPT           = ('[្]', 'SUB')
END_SIGN            = ('[៓-៝]', 'END')
ZERO_WIDTH_SPACE    = ('\u200b', 'ZS')
NUMBER              = ('[០-៩0-9]', 'NS')
LATIN               = ('[a-zA-ZÀ-ÿ]', 'NS')
UNKNOWN             = ('', 'UNK')

_CHAR_TYPES = [
    CONSONANT,
    VOWEL,
    IND_VOWEL,
    UPPER_SIGN,
    ATAK_NUMBER,
    LUNAR_NUMBER,
    SUBSCRIPT,
    END_SIGN,
    NUMBER,
    LATIN,
    ZERO_WIDTH_SPACE,
    UNKNOWN
]

#### char type

def get_char_type(prev_char: str, char: str, next_char: str):
    # number
    if (char in [',', '.']) and bool(re.match(NUMBER[0], prev_char)) and bool(re.match(NUMBER[0], next_char)):
        return NUMBER[1]

    char_type = None
    for regx, type_ in _CHAR_TYPES:
        if bool(re.match(regx, char)) is True:
            char_type = type_
            break

    return char_type if char_type is not None else UNKNOWN[1]

#### crf feature

def char2features(sent, i):
    features = {
        'char': sent[i][0],
        'type': sent[i][1]
    }

    # char[-3]
    if i > 2:
        features.update({
            'char[-3]': sent[i - 3][0],
            'type[-3]': sent[i - 3][1],
            'char[-3:-2]': sent[i - 3][0] + sent[i - 2][0],
            'char[-3:-1]': sent[i - 3][0] + sent[i - 2][0] + sent[i - 1][0],
            'char[-3:0]': sent[i - 3][0] + sent[i - 2][0] + sent[i - 1][0] + sent[i][0]
        })

    # char[-2]
    if i > 1:
        features.update({
            'char[-2]': sent[i - 2][0],
            'type[-2]': sent[i - 2][1],
            'char[-2:-1]': sent[i - 2][0] + sent[i - 1][0],
            'char[-2:0]': sent[i - 2][0] + sent[i - 1][0] + sent[i][0]
        })

    # char[-1]
    if i > 0:
        features.update({
            'char[-1]': sent[i - 1][0],
            'type[-1]': sent[i - 1][1],
            'char[-1:0]': sent[i - 1][0] + sent[i][0]
        })
    else:
        features['BOS'] = True

    # char[+1]
    if i < len(sent) - 1:
        features.update({
            'char[+1]': sent[i + 1][0],
            'type[+1]': sent[i + 1][1],
            'char[0:+1]': sent[i][0] + sent[i + 1][0]
        })
    else:
        features['EOS'] = True

    # char[+2]
    if i < len(sent) - 2:
        features.update({
            'char[+2]': sent[i + 2][0],
            'type[+2]': sent[i + 2][1],
            'char[+1:+2]': sent[i + 1][0] + sent[i + 2][0],
            'char[0:+2]': sent[i][0] + sent[i + 1][0] + sent[i + 2][0]
        })

    # char[+3]
    if i < len(sent) - 3:
        features.update({
            'char[+3]': sent[i + 3][0],
            'type[+3]': sent[i + 3][1],
            'char[+2:+3]': sent[i + 2][0] + sent[i + 3][0],
            'char[+1:+3]': sent[i + 1][0] + sent[i + 2][0] + sent[i + 3][0],
            'char[0:+3]': sent[i][0] + sent[i + 1][0] + sent[i + 2][0] + sent[i + 3][0]
        })

    return features

def sent2features(sent):
    return [char2features(sent, i) for i in range(len(sent))]

def sent2chars(sent):
    return [e[0] for e in sent]

def sent2types(sent):
    return [e[1] for e in sent]


#### other

def export_vocab(corpus_files, output_file, vocab_size=None, reverse_sort=True, export_wcount=True,
                 in_filters=[], out_filters=[]):
    vocab_counter = Counter()

    # read files
    for file in corpus_files:
        print('Read train file: %s' % file)
        with open(file, 'r', encoding='utf-8') as reader:
            for line in tqdm(reader):
                word_map = {}
                for word in line.split():

                    # apply filters
                    skip_word = False
                    for filter_ in in_filters:
                        if bool(re.match(r'%s' % filter_, word)) is False:
                            skip_word = True
                            break

                    for filter_ in out_filters:
                        if bool(re.match(r'%s' % filter_, word)) is True:
                            skip_word = True
                            break

                    if skip_word is True:
                        continue

                    num = word_map.get(word)
                    if num is None:
                        word_map[word] = 1
                    else:
                        word_map[word] = num + 1

                vocab_counter.update(word_map)

    # write vocab
    print('Write vocab %s ' % output_file)
    with open(output_file, 'w') as writer:
        lexicon = sorted(vocab_counter.most_common(vocab_size), key=lambda item: item[1], reverse=reverse_sort)

        for word, n in lexicon:
            if export_wcount is True:
                writer.write('%s %s\n' % (word, n))
            else:
                writer.write('%s\n' % word)

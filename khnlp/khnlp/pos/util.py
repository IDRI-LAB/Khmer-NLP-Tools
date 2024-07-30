def token2features(sent, i):
    features = {
        'token': sent[i][0],
    }

    # token[-3]
    if i > 2:
        features.update({
            'token[-3]': sent[i - 3][0],
            'token[-3:-2]': sent[i - 3][0] + sent[i - 2][0],
            'token[-3:-1]': sent[i - 3][0] + sent[i - 2][0] + sent[i - 1][0],
            'token[-3:0]': sent[i - 3][0] + sent[i - 2][0] + sent[i - 1][0] + sent[i][0]
        })

    # token[-2]
    if i > 1:
        features.update({
            'token[-2]': sent[i - 2][0],
            'token[-2:-1]': sent[i - 2][0] + sent[i - 1][0],
            'token[-2:0]': sent[i - 2][0] + sent[i - 1][0] + sent[i][0]
        })

    # token[-1]
    if i > 0:
        features.update({
            'token[-1]': sent[i - 1][0],
            'token[-1:0]': sent[i - 1][0] + sent[i][0]
        })
    else:
        features['BOS'] = True

    # token[+1]
    if i < len(sent) - 1:
        features.update({
            'token[+1]': sent[i + 1][0],
            'token[0:+1]': sent[i][0] + sent[i + 1][0]
        })
    else:
        features['EOS'] = True

    # token[+2]
    if i < len(sent) - 2:
        features.update({
            'token[+2]': sent[i + 2][0],
            'token[+1:+2]': sent[i + 1][0] + sent[i + 2][0],
            'token[0:+2]': sent[i][0] + sent[i + 1][0] + sent[i + 2][0]
        })

    # token[+3]
    if i < len(sent) - 3:
        features.update({
            'token[+3]': sent[i + 3][0],
            'token[+2:+3]': sent[i + 2][0] + sent[i + 3][0],
            'token[+1:+3]': sent[i + 1][0] + sent[i + 2][0] + sent[i + 3][0],
            'token[0:+3]': sent[i][0] + sent[i + 1][0] + sent[i + 2][0] + sent[i + 3][0]
        })

    return features

def sent2features(sent):
    return [token2features(sent, i) for i in range(len(sent))]

def sent2tokens(sent):
    return [e[0] for e in sent]

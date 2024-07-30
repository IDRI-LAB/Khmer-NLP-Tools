def load_data(files: [str]):
    X = []
    y = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as reader:
            sample = []
            for line in reader:
                if line.startswith('#') or line == '\n':
                    if len(sample) > 1:
                        X.append(sample[0])
                        y.append(sample[1])
                        sample = []
                else:
                    line = line.strip()
                    sample.append(line.split('\t'))

            if len(sample) > 1:
                X.append(sample[0])
                y.append(sample[1])
    return X, y


def char2features(name, i):
    char = name[i][0]

    features = {
        'char': char,
    }

    # char[-3]
    if i > 2:
        features.update({
            'char[-3]': name[i - 3][0],
            'char[-3:-2]': name[i - 3][0] + name[i - 2][0],
            'char[-3:-1]': name[i - 3][0] + name[i - 2][0] + name[i - 1][0],
            'char[-3:0]': name[i - 3][0] + name[i - 2][0] + name[i - 1][0] + name[i][0]
        })

    # char[-2]
    if i > 1:
        features.update({
            'char[-2]': name[i - 2][0],
            'char[-2:-1]': name[i - 2][0] + name[i - 1][0],
            'char[-2:0]': name[i - 2][0] + name[i - 1][0] + name[i][0]
        })

    # char[-1]
    if i > 0:
        features.update({
            'char[-1]': name[i - 1][0],
            'char[-1:0]': name[i - 1][0] + name[i][0]
        })
    else:
        features['BOS'] = True

    # char[+1]
    if i < len(name) - 1:
        features.update({
            'char[+1]': name[i + 1][0],
            'char[0:+1]': name[i][0] + name[i + 1][0]
        })
    else:
        features['EOS'] = True

    # char[+2]
    if i < len(name) - 2:
        features.update({
            'char[+2]': name[i + 2][0],
            'char[+1:+2]': name[i + 1][0] + name[i + 2][0],
            'char[0:+2]': name[i][0] + name[i + 1][0] + name[i + 2][0]
        })

    # char[+3]
    if i < len(name) - 3:
        features.update({
            'char[+3]': name[i + 3][0],
            'char[+2:+3]': name[i + 2][0] + name[i + 3][0],
            'char[+1:+3]': name[i + 1][0] + name[i + 2][0] + name[i + 3][0],
            'char[0:+3]': name[i][0] + name[i + 1][0] + name[i + 2][0] + name[i + 3][0]
        })

    return features


def name2features(name):
    return [char2features(name, i) for i in range(len(name))]


def name2chars(name):
    return [c[0] for c in name]

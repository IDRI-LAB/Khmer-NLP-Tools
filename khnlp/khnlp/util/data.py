from random import Random

from tqdm import tqdm


def load_simple_data(paths: [str], preprocess=lambda x: x, random=False, random_state=None):
    dataset = []
    for file in paths:
        print('Loading data: %s' % file)
        with open(file, 'r', encoding='utf-8') as reader:
            for line in tqdm(reader):
                line = line.strip()
                if line == '':
                    continue

                sample = preprocess(line)
                if sample is None:
                    continue
                else:
                    dataset.append(sample)

    if random is True:
        dataset = random_list(dataset, random_state)

    return dataset


def random_list(data: [], random_state=None):
    new_data = data.copy()
    Random(random_state).shuffle(new_data)
    return new_data


def remove_duplicated(data: []):
    return list(set(data))

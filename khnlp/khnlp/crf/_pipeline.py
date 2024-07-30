import warnings

import scipy
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV, train_test_split

warnings.filterwarnings('ignore')

import pickle
from collections import Counter

import sklearn_crfsuite
from sklearn_crfsuite import metrics

from khnlp.util.data import load_simple_data
from khnlp.util.file import make_dirs

DEFAULT_HYPERPARAMETERS = {
    'algorithm': 'lbfgs',
    'c1': 0.1,
    'c2': 0.1,
    'max_iterations': 100,
    'all_possible_transitions': True,
    'verbose': True
}


def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))


def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-8s %s" % (weight, label, attr))


def train(train_files: [str], test_files: [str], output_dir: str, load_data, data2features, eval_trainset=False,
          params={}):
    if load_data is None:
        load_data = load_simple_data

    make_dirs(output_dir)

    # load dataset
    print('--> Loading datasets...')
    X_train, y_train = load_data(train_files)
    X_test, y_test = load_data(test_files)

    # generate crf features
    print('--> Pre-processing features: train set...')
    X_train = [data2features(s) for s in X_train]

    print('--> Pre-processing features: test set...')
    X_test = [data2features(s) for s in X_test]

    # train
    print('--> Training...')
    final_params = {}
    final_params.update(DEFAULT_HYPERPARAMETERS)
    final_params.update(params)

    crf = sklearn_crfsuite.CRF(**final_params)
    crf.fit(X_train, y_train)

    # train set
    if eval_trainset is True:
        print('--> Testing with train set...')
        y_pred = crf.predict(X_train)
        f1_score = metrics.flat_f1_score(y_train, y_pred, average='weighted')
        print('f-score: ', f1_score)

        # classification report
        print(metrics.flat_classification_report(y_train, y_pred, digits=3))

    # test set
    print('--> Testing with test set...')
    y_pred = crf.predict(X_test)
    f1_score = metrics.flat_f1_score(y_test, y_pred, average='weighted')
    print('f-score: ', f1_score)

    # classification report
    print(metrics.flat_classification_report(y_test, y_pred, digits=3))

    # show learning features and transition
    print("--> Top positive:")
    print_state_features(Counter(crf.state_features_).most_common(30))

    print("\nTop negative:")
    print_state_features(Counter(crf.state_features_).most_common()[-30:])

    print("\nTop likely transitions:")
    print_transitions(Counter(crf.transition_features_).most_common(20))

    print("\nTop unlikely transitions:")
    print_transitions(Counter(crf.transition_features_).most_common()[-20:])

    # export model
    print("\n--> Exporting model...")
    model_file = '%s/model.bin' % output_dir
    with open(model_file, 'wb') as writer:
        pickle.dump(crf, writer)


def test(model_file: str, test_files: [str], output_dir: str, load_data, data2features):
    if load_data is None:
        load_data = load_simple_data

    make_dirs(output_dir)

    # load dataset
    print('--> Loading dataset...')
    X_test, y_test = load_data(test_files)

    # generate crf features
    print('--> Pre-processing: test set...')
    X_test = [data2features(s) for s in X_test]

    # load crf model
    print('--> Loading model...')
    model = open(model_file, 'rb')
    crf = pickle.load(model)

    print('--> Testing with dataset...')
    y_pred = crf.predict(X_test)
    f1_score = metrics.flat_f1_score(y_test, y_pred, average='weighted')
    print('f-score: ', f1_score)

    # classification report
    print(metrics.flat_classification_report(y_test, y_pred, digits=3))

    model.close()

def tuning_params_with_random_cv(eval_files: [str], load_data, data2features, params_space=None,
                                 default_params=None, scorer=None, eval_size=None, cv=5, random_state=None, n_jobs=-1,
                                 n_iter=10):
    # load dataset
    print('--> Loading datasets...')
    X_eval, y_eval = load_data(eval_files)
    if eval_size is not None:
        _, X_eval, _, y_eval = train_test_split(X_eval, y_eval, test_size=eval_size, random_state=random_state)

    print('--> Pre-processing features: eval set...')
    X_eval = [data2features(s) for s in X_eval]

    final_params = {}
    final_params.update({
        'algorithm': 'lbfgs',
        'max_iterations': 100,
        'all_possible_transitions': True,
    })
    if default_params is not None:
        final_params.update(**default_params)

    crf = sklearn_crfsuite.CRF(**final_params)

    if params_space is None:
        params_space = {
            'c1': scipy.stats.expon(scale=0.5),
            'c2': scipy.stats.expon(scale=0.05),
        }

    if scorer is None:
        scorer = make_scorer(metrics.flat_f1_score, average='weighted')

    print('--> Searching params: eval set...')
    rs = RandomizedSearchCV(crf, params_space,
                            cv=cv,
                            verbose=1,
                            n_jobs=n_jobs,
                            n_iter=n_iter,
                            scoring=scorer)

    rs.fit(X_eval, y_eval)

    print('--> Search result: ')
    print('best params:', rs.best_params_)
    print('best CV score:', rs.best_score_)
    return rs.best_params_

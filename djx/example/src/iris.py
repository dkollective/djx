import os
import pandas as pd
import uuid
from joblib import dump
from time import sleep
from structlog import get_logger
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import SGDClassifier

DATA_FOLDER = 'data'
logger = get_logger()


def load_dataset(dataset, test_size, target_column, feature_columns):
    df = pd.read_csv(dataset)
    X = df[feature_columns]
    y = df[target_column]
    return X, y


def cross_val_model(X, y, model_args, cross_val_args):
    cv = StratifiedKFold(**cross_val_args)
    final_scores = []
    classes = y.unique()

    for i, (train_index, test_index) in enumerate(cv.split(X, y)):
        log = logger.bind(cross_val_split=i)
        clf = SGDClassifier(**model_args)
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        for j in range(10):
            clf.partial_fit(
                X_train.iloc[j::10], y_train.iloc[j::10], classes=classes)
            sleep(1)
            score = clf.score(X_test, y_test)
            log.info('partial fit', accuracy=score, batch=j)
        log.info('complete fit', accuracy=score, complete=True)
        final_scores.append({'cross_val_split': i, 'accuracy': score})
    return final_scores


def fit_and_save(X, y, model_args):
    local_model_path = os.path.join(DATA_FOLDER, uuid.uuid4().hex + '.pkl')
    clf = SGDClassifier(**model_args)
    clf.fit(X, y)
    dump(clf, local_model_path)
    return local_model_path


def cv_fit_save(data, *, model_args, dataset_args, cross_val_args):
    X, y = load_dataset(data['dataset'], **dataset_args)
    scores = cross_val_model(X, y, model_args, cross_val_args)
    local_model_path = fit_and_save(X, y, model_args)
    return {'model': local_model_path}, scores

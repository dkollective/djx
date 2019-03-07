import os
import pandas as pd
import uuid
from time import sleep
from structlog import get_logger
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import SGDClassifier

DATA_FOLDER = os.environ['DJX_DATA']
log = get_logger()


def load_dataset(dataset, test_size, target_column, feature_columns):
    df = pd.DataFrame.from_csv(dataset)
    X = df[feature_columns]
    y = df[target_column]
    return X, y


def cross_val_model(X, y, model_args, cross_val_args):
    cv = StratifiedKFold(**cross_val_args)
    final_scores = []
    for i, (train_index, test_index) in enumerate(cv.split(X, y)):
        log.bind(cross_val_split=i)
        clf = SGDClassifier(**model_args)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        for j in range(10):
            clf.partial_fit(X_train[j::10], y_train[j::10])
            sleep(1)
            score = clf.score(X_test, y_test)
            log.info('partial fit', accuracy=score, batch=j)
        log.info('complete fit', accuracy=score, complete=True)
        final_scores.append({'cross_val_split': i, 'accuracy': score})
    return final_scores


def fit_and_save(X, y, model_args):
    model_uuid = uuid.uuid4().hex
    clf = SGDClassifier(**model_args)
    clf.fit(X, y)
    clf.save(os.path.join(DATA_FOLDER, model_uuid))
    return model_uuid


def cv_fit_save(dataset, *, model_args, dataset_args, cross_val_args):
    X, y = load_dataset(dataset, **dataset_args)
    scores = cross_val_model(X, y, model_args, cross_val_args)
    model_uuid = fit_and_save(X, y, model_args)
    return {'model': model_uuid, 'scores': scores}

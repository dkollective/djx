import pandas as pd
# import joblib
# import djx.record
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier


def cv_fit_save(model_args, dataset_args, cross_val_args, save):
    X, y = load_dataset(**dataset_args)
    cross_val(X, y, model_args, cross_val_args)
    if save:
        fit_save(X, y, model_args)


def load_dataset(target_column, feature_columns):
    df = pd.read_csv('https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/d546eaee765268bf2f487608c537c05e22e4b221/iris.csv')
    X = df[feature_columns].values
    y = df[target_column].values
    return X, y


def cross_val(X, y, model_args, cross_val_args):
    cv = KFold(**cross_val_args)
    clf = RandomForestClassifier(**model_args)
    for i, (train_index, test_index) in enumerate(cv.split(X, y)):
        # djx.record.bind(cross_val_itteration=i)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        in_acc = clf.score(X_train, y_train)
        out_acc = clf.score(X_test, y_test)
        # djx.record.rec(
        #         'cv fit finished',
        #         metrics={'accuracy': in_acc},
        #         context={'set': 'train'})
        # djx.record.rec(
        #         'cv fit finished',
        #         metrics={'accuracy': out_acc},
        #         context={'set': 'test'})


def fit_save(X, y, model_args):
    # temp_path = djx.record.get_temp_path()
    clf = RandomForestClassifier(**model_args)
    clf.fit(X, y)
    acc = clf.score(X, y)
    # joblib.dump(clf, temp_path)
    # djx.record.rec(
    #     'fit finished',
    #     metrics={'accuracy': acc},
    #     context={'set': 'all'},
    #     artifacts={'model': temp_path})

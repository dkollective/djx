import pandas as pd
import pydantic
import yaml
import json
import sys
from typing import Optional
from pydantic import Field
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier


class Config(pydantic.BaseModel):
    labels: Optional[dict] = Field(default_factory=dict)
    cross_val_args: dict
    model_args: dict
    dataset_args: dict
    output_path: str

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)


def write_jsonl(filename, data: list[dict]):
    with open(filename, 'a') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def cv_fit(config: Config):
    X, y = load_dataset(**config.dataset_args)
    cross_val(X, y, config)


def load_dataset(target_column, feature_columns):
    df = pd.read_csv('https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/d546eaee765268bf2f487608c537c05e22e4b221/iris.csv')
    X = df[feature_columns].values
    y = df[target_column].values
    return X, y


def write_metrics(config: Config, i: int, in_acc: float, out_acc: float):
    labels = {
        **config.labels,
        'cv_split': i,
    }
    data = [
        {
            **labels,
            'metric': 'accuracy',
            'set': 'test',
            'value': out_acc,
        },
        {
            **labels,
            'metric': 'accuracy',
            'set': 'train',
            'value': in_acc,
        },
    ]   
    write_jsonl(config.output_path, data)


def cross_val(X, y, config: Config):
    cv = KFold(**config.cross_val_args)
    clf = RandomForestClassifier(**config.model_args)
    for i, (train_index, test_index) in enumerate(cv.split(X, y)):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        in_acc = clf.score(X_train, y_train)
        out_acc = clf.score(X_test, y_test)

        write_metrics(config, i, in_acc, out_acc)


if __name__ == '__main__':
    config_file = sys.argv[1]
    config = Config.load(config_file)
    cv_fit(config)
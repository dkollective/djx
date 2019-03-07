import importlib
import yaml
import subprocess
import sys
import os


def get_method(name):
    splitted = name.split('.')
    module_name = '.'.join(splitted[:-1])
    method_name = splitted[-1]
    module = importlib.import_module(module_name)
    func = getattr(module, method_name)
    return func


def get_file(func):
    module = func.__module__
    module = sys.modules[module]
    return module.__file__


def load_yaml(file_name):
    with open(file_name, 'r') as f:
        return yaml.load(f.read())


def get_git_info(entry):
    func = get_method(entry)
    folder = os.path.dirname(get_file(func))
    commit = subprocess.check_output(
        ['git rev-parse HEAD'], shell=True, cwd=folder).decode()
    repo = subprocess.check_output(
        ['git config --get remote.origin.url'], shell=True, cwd=folder).decode()
    return repo, commit

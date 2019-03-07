import importlib
import yaml
import subprocess
import sys
import md5
import os
from urllib.request import urlretrieve
from shutil import copyfile


DATA_FOLDER = os.environ['DJX_DATA']


def get_method(name):
    splitted = name.split('.')
    module_name = '.'.join(splitted[:-1])
    method_name = splitted[-1]
    module = importlib.import_module(module_name)
    func = getattr(module, method_name)
    return func


def get_local_path(remote):
    file_id = md5.hex(remote).hexdigest()
    return os.path.join(DATA_FOLDER, file_id)


def load_file(remote, local):
    if remote[0:5] == 'http':
        urlretrieve(remote, local)
    elif remote[0] == '/':
        copyfile(remote, local)
    else:
        ValueError(f'Unkown data source {remote}')


def store_file(local, remote):
    if remote[0] == '/':
        copyfile(local, remote)
    else:
        ValueError(f'Unkown data store {remote}')


def check_local(local_path):
    return os.path.isfile(local_path)


def get_data(remote):
    local_path = get_local_path(remote)
    if not check_local(local_path):
        load_file(remote, local_path)
    return local_path


def get_all_data(data):
    return [get_data(remote) for remote in data]


def store_data(data, ouput_prefix):
    remote_paths = {}
    for name, local_path in data.items():
        _, extension = os.path.splitext(local_path)
        remote_path = os.path.join(ouput_prefix, name + "." + extension)
        store_file(local_path, remote_path)
        remote_paths[name] = remote_path
    return remote_paths


def get_file(func):
    module = func.__module__
    module = sys.modules[module]
    return module.__file__


def load_yaml(file_name):
    with open(file_name, 'r') as f:
        return yaml.load(f.read())


def get_git_info(entry, **kwargs):
    func = get_method(entry)
    folder = os.path.dirname(get_file(func))
    commit = subprocess.check_output(
        ['git rev-parse HEAD'], shell=True, cwd=folder).decode()
    repo = subprocess.check_output(
        ['git config --get remote.origin.url'], shell=True, cwd=folder).decode()
    return repo, commit

from hashlib import md5
import os
from urllib.request import urlretrieve
from shutil import copyfile


DATA_TEMP = os.environ['DJX_DATA_TEMP']
DATA_STORE = os.environ['DJX_DATA_STORE']


def create_temp_path(remote):
    file_id = md5(remote).hexdigest()
    return os.path.join(DATA_TEMP, file_id)


def load_file(remote, temp):
    if remote[0:5] == 'http':
        urlretrieve(remote, temp)
    elif remote[0] == '/':
        copyfile(remote, temp)
    else:
        ValueError(f'Unkown data source {remote}')


def store_file(temp, remote):
    if remote[0] == '/':
        copyfile(temp, remote)
    else:
        ValueError(f'Unkown data store {remote}')


def check_temp(temp_path):
    return os.path.isfile(temp_path)


def get_data(remote):
    temp_path = create_temp_path(remote)
    if not check_temp(temp_path):
        load_file(remote, temp_path)
    return temp_path


def get_all_data(data):
    return [get_data(remote) for remote in data]


def store_data(data):
    remote_paths = {}
    for name, temp_path in data.items():
        _, extension = os.path.splitext(temp_path)
        remote_path = os.path.join(DATA_STORE, name + "." + extension)
        store_file(temp_path, remote_path)
        remote_paths[name] = remote_path
    return remote_paths

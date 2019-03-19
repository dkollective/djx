from hashlib import md5
import os
from djx.data_utils import check_file, copy_file
from djx.job import get_data_path


DATA_TEMP = os.environ['DJX_DATA_TEMP']
DATA_STORE = os.environ['DJX_DATA_STORE']


def load(loader, name):
    path = get_data_path(name)
    local_path = local_from_remote(path)
    return loader(local_path)


def get_path(name):
    return get_data_path(name)


def local_from_remote(remote):
    if (remote[:len(DATA_STORE)] == DATA_STORE) and check_file(remote):
        local = DATA_TEMP + remote[len(DATA_STORE):]
        if not check_file(local):
            copy_file(remote, local)
        return local
    else:
        raise ValueError(f'Remote file path {remote} not in DJX_DATA_STORE.')


def create_paths(source, timestamp):
    file_id = md5((source + timestamp).encode()).hexdigest()
    return os.path.join(DATA_TEMP, file_id), os.path.join(DATA_STORE, file_id)


def get_data(source, timestamp):
    local_path, remote_path = create_paths(source, timestamp)
    found_temp = check_file(local_path)
    found_remote = check_file(remote_path)
    if not found_temp and not found_remote:
        copy_file(source, local_path)
        copy_file(local_path, remote_path)
    elif not found_temp and found_remote:
        copy_file(found_remote, local_path)
    elif found_temp and not found_remote:
        copy_file(found_temp, found_remote)
    return local_path, remote_path


def get_all_data(data):
    local = {}
    remote = {}
    for k, v in data.items():
        local_path, remote_path = get_data(**v)
        local[k] = local_path
        remote[k] = remote_path
    return local, remote

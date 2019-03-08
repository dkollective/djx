from hashlib import md5
import os
import re
from urllib.request import urlretrieve
from shutil import copyfile
from google.cloud import storage


DATA_TEMP = os.environ['DJX_DATA_TEMP']
DATA_STORE = os.environ['DJX_DATA_STORE']


def gs_upload(source, destination):
    bucket_name, blob_name = re.match('gs://(*?)/(*)', destination)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source)


def gs_download(source, destination):
    bucket_name, blob_name = re.match('gs://(*?)/(*)', source)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination)


def gs_check(filename):
    bucket_name, blob_name = re.match('gs://(*?)/(*)', filename)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=blob_name, delimiter=None)
    return next(blobs) is not None


def create_paths(source):
    file_id = md5(source).hexdigest()
    return os.path.join(DATA_TEMP, file_id), os.path.join(DATA_STORE, file_id)


def create_store_path(source):
    file_id = md5(source).hexdigest()
    return os.path.join(DATA_STORE, file_id)


def copy_file(source, destination):
    if source[0:5] == 'http' and destination[0] == '/':
        urlretrieve(source, destination)
    elif source[0] == '/' and destination[0] == '/':
        copyfile(source, destination)
    elif source[0] == '/' and destination[0:2] == 'gs':
        gs_upload(source, destination)
    elif source[0:2] == 'gs' and destination[0] == '/':
        gs_download(source, destination)
    else:
        ValueError(
            f'Unkown source {source} and destination {destination} combination.')


def check_file(filename):
    if filename[0] == '/':
        return os.path.isfile(filename)
    elif filename[0:2] == 'gs':
        return gs_check(filename)


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


def get_data(source):
    local_path, remote_path = create_paths(source)
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
    for k, v in data:
        local_path, remote_path = get_data(v)
        local[k] = local_path
        remote[k] = remote_path
    return local, remote


def store_data(data):
    remote_paths = {}
    for name, temp_path in data.items():
        _, extension = os.path.splitext(temp_path)
        remote_path = os.path.join(DATA_STORE, name + "." + extension)
        copy_file(temp_path, remote_path)
        remote_paths[name] = remote_path
    return remote_paths

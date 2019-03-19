import os
import re
import logging
from urllib.request import urlretrieve
from shutil import copyfile
from google.cloud import storage

log = logging.getLogger(__name__)


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


def copy_file(source, destination):
    if source[0:4] == 'http' and destination[0] == '/':
        log.info(f'Load from url: {source}')
        urlretrieve(source, destination)
    elif os.path.isfile(source) and destination[0] == '/':
        log.info(f'Copy from folder: {source}')
        copyfile(source, destination)
    elif os.path.isfile(source) and destination[0:2] == 'gs':
        log.info(f'Copy from folder to gs: {source}')
        gs_upload(source, destination)
    elif source[0:2] == 'gs' and destination[0] == '/':
        log.info(f'Copy from gs to folder: {source}')
        gs_download(source, destination)
    else:
        raise ValueError(
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

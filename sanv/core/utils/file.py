from __future__ import unicode_literals
import os
import time
import uuid
from django.core.files.storage import FileSystemStorage


def normalize_file_path(file, subpath):
    # Get new filename
    name = file.name
    ext = name[name.rfind('.'):len(name)] # Get file extension
    timestamp = str(time.time()).replace('.', '')
    uuid_str = uuid.uuid4().hex[:16]
    file_name = "{}_{}{}".format(timestamp, uuid_str, ext)
    # Get new path
    file_path = os.path.join(subpath, file_name)
    return file_path

def handle_file_upload(file, **kwargs):
    """
    Handle upload file
    """
    print(file.__dict__)
    subpath = kwargs.pop('subpath') if 'subpath' in kwargs.keys() else None
    fp = normalize_file_path(file, subpath)
    fs = FileSystemStorage()
    file_path = fs.save(fp, file)
    file_url = fs.url(file_path)
    return file_url

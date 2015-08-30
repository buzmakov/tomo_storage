from uuid import uuid4
import shutil
import os
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.storage
files_collection = db.files


def _build_name_by_id(file_id):
    data_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../data/files')
    )
    return os.path.join(data_folder, file_id)


def store_file(file_name, file_tags=None):
    if not os.path.isfile(file_name):
        return {'status': 'File not found'}
    else:
        file_id = str(uuid4())
        out_file_name = _build_name_by_id(file_id)
        if not os.path.isfile(out_file_name):
            shutil.copyfile(file_name, out_file_name)
        file_info = {'file_id': file_id, 'path': out_file_name}
        if (file_tags is not None) and isinstance(file_tags, dict):
            file_info.update(file_tags)
        files_collection.insert(file_info)
        return {'status': 'ok', 'file_id': file_id}


def get_file_info(file_id):
    file_info = files_collection.find_one({'file_id': file_id})
    file_name = file_info['path']
    if os.path.isfile(file_name):
        return {'status': 'ok', 'file_name': file_name}
    else:
        return {'status': 'File not found'}


def delete_file(file_id):
    files_count = files_collection.count({'file_id': file_id})
    if not files_count == 0:
        for file_info in files_collection.find({'file_id': file_id}):
            file_info = file_info
            file_name = file_info['path']
            try:
                os.remove(file_name)
            except OSError:
                pass
        files_collection.delete_many({'file_id': file_id})
        return {'status': 'ok', 'file_id': file_id}
    else:
        return {'status': 'File not found'}


def get_files_list():
    file_ids = [files_cursor['file_id']
                for files_cursor in files_collection.find()]
    return file_ids

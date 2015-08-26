# from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017/')
from uuid import uuid4


def store_file():
    file_id = uuid4()
    return file_id

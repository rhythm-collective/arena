# -*- coding: utf-8 -*-
"""
arena.core.sample

Sample module for testing mongodb and nng functionality.
"""

from pymongo import MongoClient


def hello_world():
    """ Say something! """

    return "Hello World!"


def hello_mongo(uri: str) -> None:
    """ Initiate a sample connection to the MongoDB Atlas cluster. """

    scratch_db = MongoClient(
        uri,
        maxPoolSize=50,
        wtimeout=2500,
    )["scratch"]

    print(scratch_db.last_status())

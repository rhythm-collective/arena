# -*- coding: utf-8 -*-
"""
arena.core.sample

Sample module for testing mongodb and nng functionality.
"""

from pymongo import MongoClient


def hello_world() -> str:
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

def hello_nng():
    from pynng import Pair0
    peer_one = Pair0()
    peer_one.listen('tcp://127.0.0.1:54321')
    peer_two = Pair0()
    peer_two.dial('tcp://127.0.0.1:54321')
    peer_one.send(b'Well hello there')
    print(peer_two.recv())
    peer_one.close()
    peer_two.close()

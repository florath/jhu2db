#!/usr/bin/env python

import pymongo
import json
import os

def mongodb_connect():
    password = os.environ['BENE_MONGODB_PASSWORD']
    client = pymongo.MongoClient("mongodb://root:%s@bene.gridpiloten.de:27017/" % password)
    db = client["jhu"]
    return db["cases"]

def read_data():
    with open("data/rki-data-20200321-1315.json") as fd:
        jdata = json.load(fd)
    return jdata

def main():
    col = mongodb_connect()
    data = read_data()
    col.insert_many(data)

if __name__ == '__main__':
    main()

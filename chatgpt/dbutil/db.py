#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/10/28 17:12
# @Author : ${飞天@小猪}
# @Email : 575566430@qq.com
# @File : db.py
# @Project : stocks
import sys
import os

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime


class DB(object):
    _instance = None
    _first_init = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,uri,dbname):
        self.uri=uri
        self.dbname=dbname
        cls = type(self)
        if not cls._first_init:
            self.db = MongoClient(uri)[dbname]
            cls._first_init = True

    def serial(self, dct):
        if dct is None:
            return None
        for k in dct:
            if isinstance(dct[k], ObjectId):
                dct[k] = str(dct[k])
            if isinstance(dct[k], datetime):
                dct[k] = datetime.strftime(dct[k], '%Y-%m-%d %H:%M:%S')
        return dct

    def find_one(self, table, filter=None):
        try:
            if filter is None:
                filter = dict()
            result = self.db[table].find_one(filter=filter)
            return self.serial(result)
        except:
            import time
            time.sleep(1)
            self.__init__(self.uri,self.dbname)
            self.find_one(table=table, filter=filter)

    def find(self, table, filter=None):
        try:
            if filter is None:
                filter = dict()
            return self.db[table].find(filter)
        except Exception as e:
            import time
            time.sleep(1)
            print("db find err",e)
            self.__init__(self.uri,self.dbname)
            self.find(table=table, filter=filter)

    # def count(self, table, filter=None):
    #     if filter is None:
    #         filter = dict()
    #     return self.db[table].count(filter=filter)

    def insert_one(self, table, data):
        try:
            self.db[table].insert_one(data)
        except Exception as e:
            print("db find err", e)
            import time
            time.sleep(1)
            self.__init__(self.uri,self.dbname)
            self.insert_one(table=table,data=data)

    def insert_many(self, table, datas):
        try:
            self.db[table].insert_many(datas)
        except Exception as e:
            print("db find err", e)
            import time
            time.sleep(1)
            self.__init__(self.uri,self.dbname)
            self.insert_many(table=table,datas=datas)

    def update_one(self, table, filter, update):
        try:
            uo = self.db[table].update_one(filter, {"$set": update})
        except Exception as e:
            print("db find err", e)
            import time
            time.sleep(1)
            self.__init__(self.uri,self.dbname)
            self.update_one(table=table,filter=filter,update=update)

    def update_many(self, table, filter, update):
        try:
            u = self.db[table].update_many(filter, {"$set": update})
        except Exception as e:
            print("db find err", e)
            import time
            time.sleep(1)
            self.__init__(self.uri,self.dbname)
            self.update_many(table=table,filter=filter,update=update)

    def delete_one(self, table, filter):
        try:
            self.db[table].delete_one(filter)
        except Exception as e:
            print("db find err", e)
            import time
            time.sleep(1)
            self.__init__(self.uri,self.dbname)
            self.delete_one(table=table,filter=filter)

    def delete_many(self, table, filter):
        try:
            self.db[table].delete_many(filter)
        except Exception as e:
            print("db find err", e)
            import time
            time.sleep(1)
            self.__init__(self.uri, self.dbname)
            self.delete_many(table=table,filter=filter)
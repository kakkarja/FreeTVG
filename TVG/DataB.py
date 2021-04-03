# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import json
import os

class Datab:
    """
    Database created in json file.
    """
    def __init__(self, name: str):
        self.name = name
        self.path = None
        self.ckname = None
        if '\\' in self.name:
            self.path = self.name.rpartition('\\')[0]
            self.ckname = self.name.rpartition('\\')[2]
        else:
            self.ckname = self.name
    
    def __str__(self):
        return f'{self.name}.json'
    
    def createdb(self, data: dict):
        # Create first time database.
        
        with open(f'{self.name}.json', 'w') as dbj:
            json.dump(data, dbj)
        data.clear()
    
    def indata(self, data: dict):
        # Insert data to existing database.
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb)) 
            with open(f'{self.name}.json', 'w') as dbj:
                json.dump(adb | data, dbj)
        else:
            print('Please create database first!')
        if adb:
            adb.clear()
        data.clear()
    
    def deldata(self, named: str):
        # Delete a data in existing database.
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb))
            if named in adb:
                del adb[named]
                with open(f'{self.name}.json', 'w') as dbj:
                    json.dump(adb, dbj)
            else:
                print('Data not exist!')
        else:
            print('Please create database first!')
        if adb:
            adb.clear()
    
    def takedat(self, named: str):
        # Taking a data from database.
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb))
            if named in adb:
                rit = adb[named]
                adb.clear()
                return rit
            else:
                print('Data not exist!')
        else:
            print('Please create database first!')
        if adb:
            adb.clear()
            
    def totalrecs(self):
        # Return the total of records in database.
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb))
            return len(adb)
        if adb:
            adb.clear()
        
    def deldb(self):
        # Delete database.
        
        if f'{self.ckname}.json' in os.listdir(self.path):
            os.remove(f'{self.name}.json')
    
    def loadall(self):
        # Load all database to dictionary's items.
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb))
            return adb.items()
        if adb:
            adb.clear()
    
    def loadkeys(self):
        # Load all database keys only.
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb))
            return adb.keys()
        if adb:
            adb.clear()
    
    def loadvalues(self):
        # Load all database values only
        
        adb = None
        if f'{self.ckname}.json' in os.listdir(self.path):
            with open(f'{self.name}.json') as rdb:
                adb = dict(json.load(rdb))
            return adb.values()
        if adb:
            adb.clear()
            
                
if __name__ == '__main__':
    a = Datab(os.path.join(os.getcwd(),'coba'))
    
    print(a)
    a.createdb({'mantaaap': 'keren'})
    a.indata({'keren': 'mantaaap'})
    print(a.totalrecs())
    print(list(a.loadall()))
    print(list(a.loadkeys()))
    print(list(a.loadvalues()))
    print(a.takedat('keren'))
    a.deldata('mantaaap')
    print(a.loadall())
    print(a.totalrecs())
    a.deldb()
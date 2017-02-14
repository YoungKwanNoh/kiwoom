from pymongo import MongoClient
import time

client = MongoClient("localhost", 27017)

def setDBEnabled(self, b):
    self.enableDB = b

def isDBEnabled(self):
    return self.enableDB

def addValue(self, dbname, tablename, json):
    db = client[dbname]
    print(json)
    if self.enableDB == True:
        db[tablename].insert_one(json)
        time.sleep(0.2)


def setLastTime(self ):

    db = client[self.dbname]
    #data = db[scode].find().sort({time:-1}).limit(1)
    cursor = db[self.tablename].find({}, sort=[('time', -1)], limit = 1)

    self.lasttime = 0

    for item in cursor:
        print("Set Last time: %d" % item['time'])
        self.lasttime = item['time']



def IsOver(self, time):
    if self.enableDB == False:
        return True

    if time > self.lasttime:
        return True

    return False

def setDatabaseName(self, month, period):
    self.dbname = month + "_" + str(period)
    print('Set Databse: %s' % self.dbname)

def setTable(self, tablename):
    self.tablename = tablename

def getDatabaseName(self):
    return self.dbname

def getTableName(self):
    return self.tablename

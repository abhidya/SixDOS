import datetime
import os

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None


MONGO_URI = os.environ.get("SIXDOS_MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.environ.get("SIXDOS_MONGO_DB", "sixdos")


def get_db():
    if MongoClient is None:
        raise RuntimeError("pymongo is not installed")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=750)
    return client[MONGO_DB]


def days_hours_minutes(td):
    return (str(td.days) + " Days " + str(td.seconds // 3600) + " Hours " + str((td.seconds // 60) % 60) + " Minutes ")


def update_chars(char_size):
    db = get_db()
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalChars'] = char_size + result['TotalChars']
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def update_tweets(tweets_size):
    db = get_db()
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalTweets'] = tweets_size + result['TotalTweets']
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def update_last(name):
    db = get_db()
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['LastPerson'] = name
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def time():
    db = get_db()
    result = db.spyder.find_one({'_id': "MBhidya"})
    return days_hours_minutes(datetime.datetime.now() - result['startTime'])


def initialize():
    db = get_db()
    post = {"TotalTweets": 0, 'TotalChars': 0, 'startTime': datetime.datetime.now(), "LastPerson": "respektor"}
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": post}, upsert=True)
    return update


def updatetotalusers():
    db = get_db()
    FIE = {'_id': True}
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalUsers'] = db.data.find(projection=FIE).count()
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update

from pymongo import MongoClient
import datetime


def days_hours_minutes(td):
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    return (str(td.days) + " Days " + str(td.seconds // 3600) + " Hours " + str((td.seconds // 60) % 60) + " Minutes ")


def update_chars(char_size):
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalChars'] = char_size + result['TotalChars']
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def update_tweets(tweets_size):
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalTweets'] = tweets_size + result['TotalTweets']
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def update_last(name):
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['LastPerson'] = name
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def time():
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    return days_hours_minutes(datetime.datetime.now() - result['startTime'])


def initialize():
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    post = {"TotalTweets": 0, 'TotalChars': 0, 'startTime': datetime.datetime.now(), "LastPerson": "respektor"}
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": post}, upsert=True)
    return update


def updatetotalusers():
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    FIE = {'_id': True}
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalUsers'] = db.data.find(projection=FIE).count()
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update

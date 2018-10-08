from pymongo import MongoClient
import datetime


def days_hours_minutes(td):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sixdos']
    return ("Days " + str(td.days) + " Hours " + str(td.seconds // 3600) + " Minutes " + str(
        (td.seconds // 60) % 60))


def update_chars(char_size):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalChars'] = char_size + result['TotalChars']
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def update_tweets(tweets_size):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    result['TotalTweets'] = char_size + result['TotalTweets']
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": result}, upsert=True)
    return update


def time():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sixdos']
    result = db.spyder.find_one({'_id': "MBhidya"})
    return days_hours_minutes(datetime.datetime.now() - result['startTime'])


def initialize():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sixdos']
    post = {"TotalTweets": 0, 'TotalChars': 0, 'startTime': datetime.datetime.now(), "LastPerson": "respektor"}
    update = db.spyder.update({'_id': "MBhidya"}, {"$set": post}, upsert=True)
    return update


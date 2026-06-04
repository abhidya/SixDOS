#!/usr/bin/env python
import json
import os
from threading import Lock
import updatestats
from flask import Flask, jsonify, render_template
# import subprocess
try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None


async_mode = None

app = Flask(__name__)

thread = None
thread_lock = Lock()

FIELDS = {'date': True}
MONGO_URI = os.environ.get("SIXDOS_MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.environ.get("SIXDOS_MONGO_DB", "sixdos")
USE_MONGO = os.environ.get("SIXDOS_USE_MONGO") == "1"
FIXTURE_DATES = [{"date": "offline-fixture", "_id": "demo-user"}]
FIXTURE_SPYDER = {
    "_id": "MBhidya",
    "TotalTweets": 0,
    "TotalChars": 0,
    "TotalUsers": 1,
    "LastPerson": "demo-user",
    "startTime": "offline-fixture",
}


def get_db():
    if MongoClient is None or not USE_MONGO:
        return None
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=750)
    return client[MONGO_DB]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify({
        "ok": True,
        "mongo": USE_MONGO and MongoClient is not None,
        "mode": "mongo" if USE_MONGO and MongoClient is not None else "offline-fixture",
    })


@app.route('/spyder.html')
def spyder():
    return render_template('spyder.html')


@app.route('/visualization', methods=['get'])
def data_visualization():
    db = get_db()
    if db is None:
        return json.dumps(FIXTURE_DATES, indent=4, sort_keys=True, default=str), 200
    projects = db.data.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
        # print(project)
    json_projects = json.dumps(json_projects, indent=4, sort_keys=True, default=str)
    return json_projects, 200




@app.route('/spyder/visualization', methods=['get'])
def spyder_visualization():
    db = get_db()
    if db is None:
        return json.dumps(FIXTURE_SPYDER, indent=4, sort_keys=True, default=str), 200
    project = db.spyder.find_one({'_id': "MBhidya"})
    if project is None:
        return json.dumps(FIXTURE_SPYDER, indent=4, sort_keys=True, default=str), 200
    project['startTime'] = updatestats.time()

    json_projects = json.dumps(project, indent=4, sort_keys=True, default=str)
    # print(json_projects)
    return json_projects, 200



if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')

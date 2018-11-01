#!/usr/bin/env python
import json
from threading import Lock
import updatestats
from flask import Flask, render_template
# import subprocess
from flask_pymongo import PyMongo
from pymongo import MongoClient


async_mode = None

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
app.config['MONGO_URI'] = "mongodb://35.185.118.72:27017/sixdos"
app.config['MONGO_USERNAME'] = 'root'
app.config['MONGO_PASSWORD'] = 'PhMb1okSjv6w'

mongo = PyMongo(app)
thread = None
thread_lock = Lock()

FIELDS = {'date': True}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/spyder.html')
def spyder():
    return render_template('spyder.html')


@app.route('/visualization', methods=['get'])
def data_visualization():
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    projects = db.data.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
        # print(project)
    json_projects = json.dumps(json_projects, indent=4, sort_keys=True, default=str)
    return json_projects, 200




@app.route('/spyder/visualization', methods=['get'])
def spyder_visualization():
    client = MongoClient("mongodb://root:PhMb1okSjv6w@35.185.118.72:27017/")
    db = client['sixdos']
    project = db.spyder.find_one({'_id': "MBhidya"})
    project['startTime'] = updatestats.time()

    json_projects = json.dumps(project, indent=4, sort_keys=True, default=str)
    # print(json_projects)
    return json_projects, 200



if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')

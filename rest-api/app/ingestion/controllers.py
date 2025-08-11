# Flask related methods...
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, send_from_directory, after_this_request, send_file
# Secure filename
from werkzeug.utils import secure_filename

# importing os module
import os

# Database
from app import db

# System libraries
from datetime import datetime
# Regular expressions libraries
import re

# Trace back libary
import traceback

# Configuration
from app import config_ as config

# Security helpers
from app.utils.utils import is_valid_session, hash_password, get_subject
from app.utils.utils import hash_string
from app.utils.utils import hash_bytes
from app.utils.utils import compute_hmac

# Datetime utilities
from datetime import date
from datetime import datetime

# Threading stuff
from time import sleep
import threading

# Logging 
import logging

# OS and representation stuff
import os
from binascii import hexlify
from json import dumps

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Database models
from app.api.models import Sensors
from app.api.models import Attributes
from app.api.models import SensorAlerts

# Import SQLAlchemy functions
from sqlalchemy.sql import func

# Temporary files
import tempfile

# Security stuff
from Crypto.Hash import SHA256

# Blueprint
mod_injection = Blueprint("injection", __name__, url_prefix="/injection")


# Cassandra cluster configuration
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from cassandra import ConsistencyLevel


cluster = Cluster(config["CASSANDRA_NODES"])
session = cluster.connect(config["CASSANDRA_KEYSPACE"])


@mod_injection.route("/add_data/", methods=["POST"])
def add_data():
    #if not is_valid_session(request, config):
    #    return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    data = data.get("points", {})

    for sensor in data.keys():
        tag = sensor
        sensor_ = db.session.query(Sensors).\
            filter(db.and_(Sensors.tag.ilike(tag))). \
                first()
        
        if not sensor_:
            continue

        insert_points = session.prepare('INSERT INTO ph (tag, date_bucket, ts, value) VALUES (?, ?, ?, ?)')
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        data_ = data[tag]["data"]
        hmac = data[tag]["hmac"]
        data_b = dumps(data_)
        
        if hmac != compute_hmac(data_b, sensor_.master_secret):
            print("Invalid HMAC")
            continue

        for p in data[tag]["data"]:
            try:
                date_object = datetime.fromtimestamp(float(p["timestamp"]) / 1000)
                bucket = date_object.strftime("%Y-%m-%d")
                batch.add(insert_points,(tag, bucket, p["timestamp"],p["value"]))
            except Exception as e:
                print(e)
                return jsonify({
                    "auth_fail": False,
                    "result": False
                })
        session.execute(batch)

    return jsonify({
        "auth_fail": False,
        "result": True
    })


@mod_injection.route("/add_alert/", methods=["POST"])
def add_alert():

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    data = data.get("alerts", {})

    for sensor in data.keys():
        tag = sensor
        
        sensor_ = db.session.query(Sensors).\
            filter(db.and_(Sensors.tag.ilike(tag))). \
                first()
        
        if not sensor_:
            continue

        data_ = data[tag]["data"]
        hmac = data[tag]["hmac"]
        data_b = dumps(data_)
        
        if hmac != compute_hmac(data_b, sensor_.master_secret):
            print("Invalid HMAC")
            continue

        for p in data[tag]["data"]:
            try:
                date_object = datetime.fromtimestamp(float(p["timestamp"]) / 1000)
                alert = SensorAlerts()
                alert.tag = tag
                alert.timestamp = date_object
                alert.type = p["type"]
                alert.comment = p["comment"]
                db.session.add(alert)
                db.session.commit()

            except Exception as e:
                print(e)
                return jsonify({
                    "auth_fail": False,
                    "result": False
                })

    return jsonify({
        "auth_fail": False,
        "result": True
    })


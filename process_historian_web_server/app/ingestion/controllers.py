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

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Database models
from app.api.models import Sensors
from app.api.models import Attributes

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
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    points = data.get("points", {})

    for sensor in points:
        tag = list(sensor.keys())[0]
        sensor_ = db.session.query(Sensors).\
            filter(db.and_(Sensors.tag.ilike(tag))). \
                first()
        
        if not sensor_:
            print("Sensor was not found in the database")
            continue

        insert_points = session.prepare('INSERT INTO ph (tag, date_bucket, ts, value) VALUES (?, ?, ?, ?)')
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        for p in sensor[tag]:
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

@mod_injection.route("/get_sensors_by_attributes/", methods=["POST"])
def get_sensors():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    attributes = data.get("attributes", [])

    sensors = db.session.query(Attributes).\
        filter(db.and_(Sensors.tag.in_(attributes))). \
            all()

    result = {}
    for sensor in sensors:
        result[sensor.tag] = True

    tags = []
    for r in result.keys():
        tags.append(r)

    return jsonify({
        "auth_fail": False,
        "result": tags
    })

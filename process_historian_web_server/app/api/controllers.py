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
mod_api = Blueprint("api", __name__, url_prefix="/api")

# Cassandra cluster configuration
from cassandra.cluster import Cluster

# Date time functions
from datetime import date, timedelta

# Cassandra cluster configuration
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from cassandra import ConsistencyLevel


cluster = Cluster(config["CASSANDRA_NODES"])
session = cluster.connect(config["CASSANDRA_KEYSPACE"])

@mod_api.route("/get_sensors/", methods=["POST"])
def get_sensors():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")

    tag = "%" + tag + "%";

    sensors = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            all()

    result = []
    for sensor in sensors:
        result.append(sensor.tag)

    return jsonify({
        "auth_fail": False,
        "result": result
    })

@mod_api.route("/get_sensors_by_attributes/", methods=["POST"])
def get_sensors_by_attributes():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    attributes = data.get("attributes", [])

    sensors = db.session.query(Attributes).\
        filter(db.and_(Attributes.attribute.in_(attributes))). \
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

@mod_api.route("/add_sensor/", methods=["POST"])
def add_sensor():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", None)
    description = data.get("description", None)
    secret = data.get("secret", None)

    attributes = data.get("attributes", [])

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()
    
    if sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor already exists"})

    sensor = Sensors()
    sensor.tag = tag
    sensor.description = description
    sensor.master_secret = secret
    db.session.add(sensor)
    db.session.commit()

    for attr in attributes:
        attribute = Attributes()
        attribute.tag = tag
        attribute.attribute = attr
        db.session.add(attribute)
        db.session.commit()

    return jsonify({
        "auth_fail": False,
        "result": True
    })

@mod_api.route("/update_sensor/", methods=["POST"])
def update_sensor():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", None)
    description = data.get("description", None)
    secret = data.get("secret", None)

    attributes = data.get("attributes", [])

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()
    
    if sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor already exists"})

    sensor.description = description
    sensor.master_secret = secret
    db.session.commit()

    attributes = db.session.query(Attributes).\
        filter(db.and_(Attributes.tag == tag)). \
            all()
    for attribute in attributes:
        db.session.delete(attribute)
        db.session.commit()

    for attr in attributes:
        attribute = Attributes()
        attribute.tag = tag
        attribute.attribute = attr
        db.session.add(attribute)
        db.session.commit()

    return jsonify({
        "auth_fail": False,
        "result": True
    })

@mod_api.route("/delete_sensor/", methods=["POST"])
def delete_sensor():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", None)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()
    
    if not sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor does not exist"})

    db.session.delete(sensor)
    db.session.commit()

    return jsonify({
        "auth_fail": False,
        "result": True
    })

@mod_api.route("/get_data_raw/", methods=["POST"])
def get_data_raw():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})

    tag = data.get("tag", None)

    format_string = "%Y-%m-%d %H:%M:%S"

    start = data.get("start", None)
    end = data.get("end", None)

    start = datetime.strptime(start, format_string)
    end = datetime.strptime(end, format_string)

    ts_start = int(start.timestamp() * 1000)
    ts_end = int(end.timestamp() * 1000)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()

    if not sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor does not exist"})
	
    buckets = []
    current_date = start
    while current_date <= end:
        formatted_date = current_date.strftime("%Y-%m-%d")
        buckets.append((tag, formatted_date))
        current_date += timedelta(days=1)

    query = "SELECT ts, value FROM ph WHERE tag = %s AND date_bucket = %s AND ts >= %s AND ts <= %s"
    result = []

    for bucket in buckets:
        rows = session.execute(query, (bucket[0], bucket[1], ts_start, ts_end, ), consistency_level=ConsistencyLevel.QUORUM)
        for row in rows:
            result.append({"timestamp": row[0].timestamp(), "value": row[1]})

    return jsonify({
        "auth_fail": False,
        "result": result
    })


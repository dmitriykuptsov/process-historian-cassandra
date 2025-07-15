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
#from cassandra.cluster import Cluster

#cluster = Cluster(config["CASSANDRA_NODES"])
#session = cluster.connect(config["CASSANDRA_KEYSPACE"])

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
    
    if sensor:
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

    start = data.get("start", None)
    end = data.get("end", None)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()
    
    if sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor does not exist"})

    return jsonify({
        "auth_fail": False,
        "result": True
    })

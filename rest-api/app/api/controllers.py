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
from app.auth.models import Users
from app.api.models import SensorPermissions

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

@mod_api.route("/get_users/", methods=["POST"])
def get_users():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    
    users = db.session.query(Users).all()

    result = []
    for user in users:
        result.append(user.username)

    return jsonify({
        "auth_fail": False,
        "result": result
    })

@mod_api.route("/add_permission_to_sensor/", methods=["POST"])
def add_permission_to_sensor():

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")
    username = data.get("username", "")
    
    owner = get_subject(request, config)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag == tag)). \
            first()
    
    if not sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor was not found"})

    user = db.session.query(Users).\
        filter(db.and_(Users.username == username)). \
            first()
    
    if not user:
        return jsonify({"auth_fail": False, "result": False, "reason": "User was not found"})
        
    permission = SensorPermissions()

    permission.tag = tag
    permission.username = username
    permission.owner = owner
    permission.allowed = True

    db.session.add(permission)
    db.session.commit()

    return jsonify({
        "auth_fail": False,
        "result": True
    })

@mod_api.route("/remove_permission_to_sensor/", methods=["POST"])
def remove_permission_to_sensor():

    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")
    username = data.get("username", "")

    owner = get_subject(request, config)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag == tag)). \
            first()
    
    if not sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor was not found"})

    user = db.session.query(Users).\
        filter(db.and_(Users.username == username)). \
            first()
    
    if not user:
        return jsonify({"auth_fail": False, "result": False, "reason": "User was not found"})
        
    permission = db.session.query(SensorPermissions).\
        filter(db.and_(SensorPermissions.tag == tag, SensorPermissions.owner == owner, 
                       SensorPermissions.username == username)). \
            first()
    
    if not permission:
        return jsonify({"auth_fail": False, "result": False, "reason": "Permission was not found"})

    db.session.remove(permission)
    db.session.commit()

    return jsonify({
        "auth_fail": False,
        "result": True
    })

@mod_api.route("/get_sensors/", methods=["POST"])
def get_sensors():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")

    offset = data.get("offset", 0)
    limit = data.get("limit", 20)
    

    username = get_subject(request, config)

    tag = "%" + tag + "%";

    sensors = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            offset(offset=offset).limit(limit=limit). \
                all()

    result = []
    for sensor in sensors:
        permission = db.session.query(SensorPermissions).\
            filter(db.and_(SensorPermissions.tag.ilike(tag), SensorPermissions.username == username)). \
                first()
        if permission or sensor.is_public_read:
            result.append(sensor.tag)

    return jsonify({
        "auth_fail": False,
        "result": result
    })

@mod_api.route("/get_sensor_own/", methods=["POST"])
def get_sensor_own():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")

    offset = data.get("offset", 0)
    limit = data.get("limit", 20)

    username = get_subject(request, config)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag), Sensors.owner == username)). \
            offset(offset=offset).limit(limit=limit). \
                first()

    s = {}
    if sensor:
        if sensor.owner == username:
            attribues = db.session.query(Attributes).filter(db.and_(Attributes.tag == sensor.tag)).all()
            s = {
                "tag": sensor.tag,
                "description": sensor.description,
                "secret": sensor.master_secret,
                "is_public": sensor.is_public_read,
                "attributes": []
            }
            for a in attribues:
                s["attributes"].append(a.attribute)

    return jsonify({
        "auth_fail": False,
        "result": s
    })

@mod_api.route("/get_sensors_own/", methods=["POST"])
def get_sensors_own():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")

    offset = data.get("offset", 0)
    limit = data.get("limit", 20)

    username = get_subject(request, config)

    tag = "%" + tag + "%";

    sensors = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag), Sensors.owner == username)). \
            offset(offset=offset).limit(limit=limit). \
                all()

    result = []
    for sensor in sensors:
        if sensor.owner == username:
            attribues = db.session.query(Attributes).filter(db.and_(Attributes.tag == sensor.tag)).all()
            s = {
                "tag": sensor.tag,
                "description": sensor.description,
                "secret": sensor.master_secret,
                "is_public": sensor.is_public_read,
                "attributes": []
            }
            for a in attribues:
                s["attributes"].append(a.attribute)
            result.append(s)

    return jsonify({
        "auth_fail": False,
        "result": result
    })

@mod_api.route("/count_own_sensors/", methods=["POST"])
def count_own_sensors():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    tag = data.get("tag", "")

    username = get_subject(request, config)

    tag = "%" + tag + "%";

    count = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag)), Sensors.owner == username). \
            count()

    return jsonify({
        "auth_fail": False,
        "result": count
    })

@mod_api.route("/get_sensors_by_attributes/", methods=["POST"])
def get_sensors_by_attributes():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True})
    data = request.get_json(force=True)
    if not data:
        return jsonify({"auth_fail": False, "result": False})
    
    username = get_subject(request, config)
    
    attributes = data.get("attributes", [])

    sensors = db.session.query(Attributes).\
        filter(db.and_(Attributes.attribute.in_(attributes))). \
            all()

    result = {}
    for sensor in sensors:
        permission = db.session.query(SensorPermissions).\
            filter(db.and_(SensorPermissions.tag == sensor.tag, SensorPermissions.username == username)). \
                first()
        if permission or sensor.is_public_read:
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
    
    owner = get_subject(request, config)
    
    username = get_subject(request, config)
    tag = data.get("tag", None)
    description = data.get("description", None)
    secret = data.get("secret", None)
    is_public_read = data.get("is_public_read", False)

    if is_public_read == "0":
        is_public_read = False

    if is_public_read == "1":
        is_public_read = True

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
    sensor.owner = owner
    sensor.is_public_read = is_public_read
    db.session.add(sensor)
    db.session.commit()

    for attr in attributes:
        attribute = Attributes()
        attribute.tag = tag
        attribute.attribute = attr
        db.session.add(attribute)
        db.session.commit()

    permission = SensorPermissions()

    permission.tag = tag
    permission.username = username
    permission.allowed = True
    permission.owner = owner

    db.session.add(permission)
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
    is_public_read = data.get("is_public_read", False)

    if is_public_read == "0":
        is_public_read = False

    if is_public_read == "1":
        is_public_read = True

    attributes = data.get("attributes", [])

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()
    
    username = get_subject(request, config)
    
    if not sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor already exists"})

    permission = db.session.query(SensorPermissions).\
        filter(db.and_(SensorPermissions.tag == sensor.tag, SensorPermissions.username == username)). \
            first()
    
    if sensor.owner != username:
        return jsonify({"auth_fail": False, "result": False, "reason": "Permission denied"})

    sensor.description = description
    sensor.master_secret = secret
    sensor.is_public_read = is_public_read
    db.session.commit()

    attributes_ = db.session.query(Attributes).\
        filter(db.and_(Attributes.tag == tag)). \
            all()
    for attribute in attributes_:
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

    username = get_subject(request, config)

    sensor = db.session.query(Sensors).\
        filter(db.and_(Sensors.tag.ilike(tag))). \
            first()
    
    if not sensor:
        return jsonify({"auth_fail": False, "result": False, "reason": "Sensor does not exist"})

    if sensor.owner != username:
        return jsonify({"auth_fail": False, "result": False, "reason": "Permission denied"})
    
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

    username = get_subject(request, config)

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
	
    permission = db.session.query(SensorPermissions).\
            filter(db.and_(SensorPermissions.tag == sensor.tag, SensorPermissions.username == username)). \
                first()
    
    if not permission and not sensor.is_public_read:
        return jsonify({"auth_fail": False, "result": False, "reason": "Permission denied"})


    buckets = []
    current_date = start
    while current_date <= end:
        formatted_date = current_date.strftime("%Y-%m-%d")
        buckets.append((tag, formatted_date))
        current_date += timedelta(days=1)

    query = "SELECT ts, value FROM ph WHERE tag = %s AND date_bucket = %s AND ts >= %s AND ts <= %s"
    result = []

    for bucket in buckets:
        statement = SimpleStatement(query, consistency_level=ConsistencyLevel.QUORUM)
        rows = session.execute(statement, (bucket[0], bucket[1], ts_start, ts_end, ))
        for row in rows:
            result.append({"timestamp": row[0].timestamp(), "value": row[1]})

    return jsonify({
        "auth_fail": False,
        "result": result
    })

@mod_api.route("/get_data_raw_public/", methods=["POST"])
def get_data_raw_public():
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
	
    if not sensor.is_public_read:
        return jsonify({"auth_fail": False, "result": False, "reason": "Permission denied"})


    buckets = []
    current_date = start
    while current_date <= end:
        formatted_date = current_date.strftime("%Y-%m-%d")
        buckets.append((tag, formatted_date))
        current_date += timedelta(days=1)

    query = "SELECT ts, value FROM ph WHERE tag = %s AND date_bucket = %s AND ts >= %s AND ts <= %s"
    result = []

    for bucket in buckets:
        statement = SimpleStatement(query, consistency_level=ConsistencyLevel.QUORUM)
        rows = session.execute(statement, (bucket[0], bucket[1], ts_start, ts_end, ))
        for row in rows:
            result.append({"timestamp": row[0].timestamp(), "value": row[1]})

    return jsonify({
        "result": result
    })


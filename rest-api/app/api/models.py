from app import db

class Sensors(db.Model):
	__tablename__ = "Sensors";

	tag                = db.Column(db.String(100),  nullable=False, primary_key=True)
	master_secret      = db.Column(db.String(200),  nullable=True)
	description        = db.Column(db.String(1000), nullable=True)
	owner              = db.Column(db.String(100), nullable = False)
	is_public_read     = db.Column(db.Integer, default=False)

class Attributes(db.Model):
	__tablename__      = "Attributes"

	tag                = db.Column(db.String(100), nullable = False, primary_key = True)
	attribute          = db.Column(db.String(1000), nullable = False, primary_key = True)


class SensorPermissions(db.Model):
	
	__tablename__      = "SensorPermissions"

	tag                = db.Column(db.String(100), nullable = False, primary_key = True)
	username           = db.Column(db.String(100), nullable = False, primary_key = True)
	owner              = db.Column(db.String(100), nullable = False)
	allowed            = db.Column(db.Boolean, nullable = False, default = True)

class SensorAlerts(db.Model):
	
	__tablename__      = "Alerts"

	tag                = db.Column(db.String(100), nullable = False, primary_key = True)
	timestamp          = db.Column(db.Date, nullable = False, primary_key = True)
	type               = db.Column(db.Integer, nullable = False, primary_key = True)
	comment            = db.Column(db.String(100), nullable = True, default = "")

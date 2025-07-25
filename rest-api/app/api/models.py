from app import db

class Sensors(db.Model):
	__tablename__ = "Sensors";

	tag                = db.Column(db.String(100),  nullable=False, primary_key=True)
	master_secret      = db.Column(db.String(200),  nullable=True)
	description        = db.Column(db.String(1000), nullable=True)

class Attributes(db.Model):
	__tablename__      = "Attributes"

	tag                = db.Column(db.String(100), nullable = False, primary_key = True)
	attribute          = db.Column(db.String(1000), nullable = False, primary_key = True)


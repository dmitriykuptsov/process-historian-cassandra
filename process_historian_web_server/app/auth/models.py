from app import db

class Users(db.Model):
    __tablename__ = "Users"
    
    username = db.Column(db.String(100), nullable=False, primary_key = True)
    password = db.Column(db.String(200), nullable=False)
    salt     = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Username %r>' % (self.username)
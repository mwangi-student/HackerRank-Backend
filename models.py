from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Users(db.Model):
    __tablename__ = "users"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False) 
    password = db.Column(db.String(512), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)

# relationship
    tm_id = db.relationship("TM", backref="users", cascade="all, delete", lazy=True)
 
class TM(db.Model):
    __tablename__ = "tm"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False) 
    password = db.Column(db.String(512), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
# from app import db
from flask_restful import fields
from sqlalchemy.sql import func
from datetime import datetime
from blueprints import db
from sqlalchemy.sql.expression import text
from sqlalchemy import Integer, ForeignKey, String, Column


class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(1000), nullable=False)
    salt = db.Column(db.String(255))
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    no_hp = db.Column(db.String(14), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "status": fields.String,
        "name": fields.String,
        "email": fields.String,
        "no_hp": fields.String,
        "alamat": fields.String,
        "avatar": fields.String,
    }

    jwt_calims_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "status": fields.String,
        "name": fields.String,
        "email": fields.String,
        "no_hp": fields.String,
        "alamat": fields.String,
        "avatar": fields.String,
    }

    def __init__(self, username, password, status, salt, name, email, no_hp, alamat, avatar):
        self.username = username
        self.password = password
        self.status = status
        self.salt = salt
        self.name = name
        self.email = email
        self.no_hp = no_hp
        self.alamat = alamat
        self.avatar = avatar

    def __repr__(self):
        return "<User %s>" % self.id

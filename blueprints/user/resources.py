import json
from flask import Blueprint, Flask, request, Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from .model import Users
from . import *
from blueprints import db, app, internal_required
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims,
)
from sqlalchemy import desc
import hashlib
import uuid


bp_user = Blueprint("user", __name__)
api = Api(bp_user)

class UserResource(Resource):

    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            return (
                marshal(qry, Users.response_fields),
                200,
                {"Content-Type": "application/json"},
            )
        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="json", required=True)
        parser.add_argument("password", location="json", required=True)
        parser.add_argument("status", location="json", type=str, default="user")
        parser.add_argument("name", location="json", required=True)
        parser.add_argument("email", location="json", required=True)
        parser.add_argument("no_hp", location="json", type=str, required=True)
        parser.add_argument("alamat", location="json")
        parser.add_argument("avatar", location="json", default="https://innorecycling.ch/wp-content/uploads/2018/01/generic-profile-avatar_352864.jpg")

        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encode = ("%s%s" % (args["password"], salt)).encode("utf-8")
        hash_pass = hashlib.sha512(encode).hexdigest()

        user = Users(args["username"], hash_pass, args["status"], salt, 
                args["name"], args["email"], args["no_hp"], args["alamat"], args["avatar"])
        try:
            db.session.add(user)
            db.session.commit()

            return (
                marshal(user, Users.response_fields),
                200,
                {"Content-Type": "application/json"},
            )
        except Exception as e:
            return {"status": "Eror"}, 403

    @jwt_required
    def put(self):
        claim = get_jwt_claims()
        claim_client_id = claim["id"]
        parser = reqparse.RequestParser()
        qry = Users.query.get(claim_client_id)
        parser.add_argument("username", location="json", default=qry.username)
        parser.add_argument("password", location="json", default=qry.password)
        parser.add_argument("status", location="json", default=qry.status)
        parser.add_argument("salt", location="json")
        parser.add_argument("name", location="json", type=str, default=qry.name)
        parser.add_argument("email", location="json", type=str, default=qry.email)
        parser.add_argument("no_hp", location="json", type=str, default=qry.no_hp)
        parser.add_argument("alamat", location="json", type=str, default=qry.alamat)
        parser.add_argument("avatar", location="json", default=qry.avatar)

        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encode = ("%s%s" % (args["password"], salt)).encode("utf-8")
        hash_pass = hashlib.sha512(encode).hexdigest()

        qry.username = args["username"]
        qry.password = hash_pass
        qry.status = args["status"]
        qry.salt = salt
        qry.name = args["name"]
        qry.email = args["email"]
        qry.no_hp = args["no_hp"]
        qry.alamat = args["alamat"]
        qry.avatar = args["avatar"]
        db.session.commit()

        return marshal(qry, Users.response_fields), 200


    @jwt_required
    def delete(self):
        claim = get_jwt_claims()
        claim_client_id = claim["id"]
        qry = Users.query.get(claim_client_id)
        db.session.delete(qry)
        db.session.commit()
        return {"status": "User deleted"}, 200


class UserList(Resource):
    def options(self):
        return {}, 200

    def __init__(self):
        pass
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
 
        args = parser.parse_args()
        offset = (args['p'] * args['rp'] - args['rp'])
        # qry = Users.query

        claim = get_jwt_claims()
        qry = Users.query.filter_by(id=claim["id"])

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))
            
        return rows[0], 200
 ###Routes
api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, "", "/<id>")

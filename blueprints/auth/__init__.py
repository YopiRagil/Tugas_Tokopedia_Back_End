from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims,
)
from ..user.model import Users
import hashlib
import uuid
from blueprints import internal_required

bp_auth = Blueprint("auth", __name__)
CORS(bp_auth)
api = Api(bp_auth)


class CreateTokenResource(Resource):
    def options(self):
        return {}, 200
    def get(self):
        # create token
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="args", required=True)
        parser.add_argument("password", location="args", required=True)
        args = parser.parse_args()

        qry = Users.query.filter_by(username=args["username"]).first()
        encode = ("%s%s" % (args["password"], qry.salt)).encode("utf-8")
        hash_pass = hashlib.sha512(encode).hexdigest()
        client_id = qry.id
        if qry.password == hash_pass:
            qry = marshal(qry, Users.jwt_calims_fields)
            token = create_access_token(identity=args["username"], user_claims=qry)
            return {"token": token, "client_id":client_id}, 200

        else:
            return {"status": "PASWORD SALAH BOSS"}, 404

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return {"claims": claims}, 200


class RefreshTokenResource(Resource):
    @jwt_required
    @internal_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {"token": token}, 200


api.add_resource(CreateTokenResource, "")
api.add_resource(RefreshTokenResource, "/refresh")

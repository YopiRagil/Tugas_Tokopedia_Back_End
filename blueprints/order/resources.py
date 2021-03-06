import json
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from .model import Orders
from .model import Users
from . import *
from blueprints import db, internal_required
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, get_jwt_claims,)
from sqlalchemy import desc
import hashlib
import uuid
import re

bp_order = Blueprint("order", __name__)
api = Api(bp_order)


class OrderResource(Resource):
    def options(self):
        return {}, 200

    def __init__(self):
        pass

    @jwt_required
    def get(self, id):
        qry = Orders.query.get(id)
        if qry is not None:
            return (
                marshal(qry, Orders.response_fields),
                200,
                {"Content-Type": "application/json"},
            )
        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("penjual_id", location="json", type=int, required=True)
        parser.add_argument("nama_pembeli", location="json", type=str, required=True)
        parser.add_argument("alamat_pembeli", location="json", type=str, required=True)
        parser.add_argument("produk_dipesan", location="json", type=str, required=True)
        parser.add_argument("harga", location="json", type=int, required=True)
        parser.add_argument("status", location="json", type=str, default="baru")
        parser.add_argument("kode_resi", location="json", type=str, required=False)

        args = parser.parse_args()

        order = Orders(
            args["penjual_id"],
            args["nama_pembeli"],
            args["alamat_pembeli"],
            args["produk_dipesan"],
            args["harga"],
            args["status"],
            args["kode_resi"],
        )
        db.session.add(order)
        db.session.commit()

        return (
            marshal(order, Orders.response_fields),
            200,
            {"Content-Type": "application/json"},
        )

    @jwt_required
    def put(self, id):
        qry = Orders.query.get(id)
        if qry is None:
            return {"status": "NOT_FOUND"}, 404

        penjual_id = qry.penjual_id
        claim = get_jwt_claims()
        user_id = claim["id"]

        if penjual_id != user_id:
            return {"status": "Access Denied", "message": "user id not allowed"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument("nama_pembeli", location="json", type=str, default=qry.nama_pembeli)
        parser.add_argument("alamat_pembeli", location="json", type=str, default=qry.alamat_pembeli)
        parser.add_argument("produk_dipesan", location="json", type=str, default=qry.produk_dipesan)
        parser.add_argument("harga", location="json", type=int, default=qry.harga)
        parser.add_argument("status", location="json", type=str, required=True)
        parser.add_argument("kode_resi", location="json", type=str, default=qry.kode_resi)

        args = parser.parse_args()

        qry.penjual_id = penjual_id
        qry.nama_pembeli = args["nama_pembeli"]
        qry.alamat_pembeli = args["alamat_pembeli"]
        qry.produk_dipesan = args["produk_dipesan"]
        qry.harga = args["harga"]
        qry.status = args["status"]
        qry.kode_resi = args["kode_resi"]

        db.session.commit()

        return marshal(qry, Orders.response_fields), 200

    @jwt_required
    def delete(self, id):
        qry = Orders.query.get(id)
        if qry is None:
            return {"status": "NOT_FOUND"}, 404

        penjual_id = qry.penjual_id
        claim = get_jwt_claims()
        user_id = claim["id"]
        if penjual_id == user_id:
            db.session.delete(qry)
            db.session.commit()
            return {"status": "Pesanan deleted"}, 200

class OrderList(Resource):
    def options(self):
        return {}, 200

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=1000)
        parser.add_argument('created_at', location='args', help='invalid status')
        parser.add_argument('start_time', location='args', help='invalid status')
        parser.add_argument('end_time', location='args', help='invalid status')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('created_at'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        parser.add_argument('keyword', location='args', help='invalid value')
        parser.add_argument('produk', location='args', help='invalid value')
        parser.add_argument('resi', location='args', help='invalid value')

        args = parser.parse_args()
        offset = (args['p'] * args['rp'] - args['rp'])

        claim = get_jwt_claims()
        qry_user = Users.query.filter_by(id=claim["id"]).first()
        penjual_id = qry_user.id
        qry = Orders.query.filter_by(penjual_id=penjual_id)
        qrysearch = qry

        if args['start_time'] is not None:
            qry = qry.filter(
                (Orders.created_at>=args['start_time']) &
                (Orders.created_at<=args['end_time'])|
                (Orders.created_at.like('%'+args['end_time']+'%'))
                )

        if args['keyword'] is not None:
            qry = qrysearch.filter(
                Orders.produk_dipesan.like('%'+args['keyword']+'%') |
                Orders.nama_pembeli.like('%'+args['keyword']+'%') | 
                Orders.kode_resi.like('%'+args['keyword']+'%') |
                Orders.alamat_pembeli.like('%'+args['keyword']+'%')
                )

        if args['orderby'] is not None:
            if args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Orders.created_at))
                else:
                    qry = qry.order_by(Orders.created_at)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Orders.response_fields))

        return rows, 200

 # Routes
api.add_resource(OrderList, "", "/semua")
api.add_resource(OrderResource, "", "/<id>")

# from app import db
from flask_restful import fields
from sqlalchemy.sql import func
from datetime import datetime
from blueprints import db
from sqlalchemy.sql.expression import text
from blueprints.user.model import Users
from sqlalchemy import Integer, ForeignKey, String, Column, Text, VARBINARY


class Orders(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    penjual_id = db.Column(db.Integer, ForeignKey(Users.id))
    nama_pembeli = db.Column(db.String(100), nullable=False)
    alamat_pembeli = db.Column(db.String(10000), nullable=False)
    produk_dipesan = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    kode_resi = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "penjual_id": fields.Integer,
        "nama_pembeli": fields.String,
        "alamat_pembeli": fields.String,
        "produk_dipesan": fields.String,
        "harga": fields.Integer,
        "status": fields.String,
        "kode_resi": fields.String,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime
    }

    def __init__(self, penjual_id, nama_pembeli, alamat_pembeli, produk_dipesan, harga, status, kode_resi):
        self.penjual_id = penjual_id
        self.nama_pembeli = nama_pembeli
        self.alamat_pembeli = alamat_pembeli
        self.produk_dipesan = produk_dipesan
        self.harga = harga
        self.status = status
        self.kode_resi = kode_resi

    def __repr__(self):
        return "<Order %s>" % self.id

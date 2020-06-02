import pytest
from app import cache, logging
import json
from flask import Flask, request, json
from blueprints import app, db
from app import cache
from blueprints.user.model import Users
from blueprints.order.model import Orders


import uuid
import hashlib


def call_client(request):
    client = app.test_client()
    return client


@pytest.fixture
def client(request):
    return call_client(request)


@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()
    salt = uuid.uuid4().hex
    encode = ('%s%s' % ('password', salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encode).hexdigest()

    user = Users(username="yopi", password=hash_pass, status="user", salt=salt,
                 name="yopi ragil", email="yopi@gmail.com", no_hp="0812333333",
                 alamat="jombang", avatar="test")
    usernonInternal = Users(username="ragil", password=hash_pass, status="admin", salt=salt,
                      name="ragil permana", email="ragil@gmail.com", no_hp="0812444444",
                      alamat="Malang", avatar="testing")
    db.session.add(user)
    db.session.add(usernonInternal)
    db.session.commit()

    order = Orders(penjual_id=1, nama_pembeli="Joni", alamat_pembeli="Jl. Tidar, Malang",
           produk_dipesan="Sikat gigi", harga=10000, status="dikirim", kode_resi="25367718",)
    db.session.add(order)
    db.session.commit()

    yield db
    db.drop_all()


def create_token():
    # prepare request
    token = cache.get('test-token')
    if token is None:
        data = {
            'username': 'yopi',
            'password': 'password',
        }
        # do request
        req = call_client(request)
        res = req.get('/auth', query_string=data)

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token', res_json['token'], timeout=60)

        return res_json['token']

    else:
        return token


def create_token_nonin():
    # prepare request
    token = cache.get('test-token-nonin')
    if token is None:
        data = {
            'username': 'ragil',
            'password': 'password',
        }

        req = call_client(request)
        res = req.get('/auth', query_string=data)

        res_json = json.loads(res.data)
        logging.warning('RESULT:%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-nonin', res_json['token'], timeout=60)

        return res_json['token']

    else:
        return token

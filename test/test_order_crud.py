import json
from . import app, client, cache, create_token, init_database

class TestOrderCrud():

    def test_order_by_id(self, client, init_database):
        token = create_token()
        res = client.get(
            '/order/1', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_order_by_id_fail(self, client, init_database):
        token = create_token()
        res = client.get(
            '/order/100', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_order(self, client, init_database):
        token = create_token()
        data={ "penjual_id": 2, 
                "nama_pembeli": "agus",
                "alamat_pembeli":"Solo", 
                "produk_dipesan":"meja belajar",
                "harga":25000,
                "kode_resi":"",
                "status":"Baru", 
            }
        res = client.post('/order', 
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
            
        res = json.loads(res.data)

    def test_order_put(self, client, init_database):
        token = create_token()
        data={ "kode_resi":"1223456",
               "status": "dikirim", 
            }
        res = client.put('/order/1',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_order_put_fail(self, client, init_database):
        token = create_token()
        data={ "kode_resi":"1223456",
               "status": "dikirim", 
            }
        res = client.put('/order/30',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_order_delete_fail(self, client, init_database):
        token = create_token()
        res = client.delete('/order/5',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res = json.loads(res.data)

    def test_order_list(self, client, init_database):
        token = create_token()
        res = client.get(
            '/order/semua', 
            headers={'Authorization':'Bearer ' + token}, 
            content_type='application/json'
            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    

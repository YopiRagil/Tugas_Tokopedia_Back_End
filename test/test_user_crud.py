import json
from . import app, client, cache, create_token, create_token_nonin, init_database


class TestUsersCrud():          
    def test_client_get_byid(self, client, init_database):
        token = create_token()
        res = client.get('/user/1',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_client_get_byid_fail(self, client, init_database):
        token = create_token()
        res = client.get('/user/3',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_post(self, client, init_database):
            token = create_token()
            data={ "username": "ajay", 
                    "password": "ajay",
                    "status": "user",
                    "name":"aji Pangestu", 
                    "email":"ajay@gmail.com",
                    "no_hp":"0812332222",
                    "alamat":"klaten", 
                    "avatar":"test",
                }
            res = client.post('/user',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            
            res_json = json.loads(res.data)
            assert res.status_code == 200
    
    def test_user_put(self, client, init_database):
        token = create_token()
        data={ "username": "asa", 
                "password": "asa",
                "name":"Asa Pangestu", 
                "email":"asa@gmail.com",
                "no_hp":"0812345422",
                "alamat":"Mojokerto", 
                "avatar":"tester",
            }
        res = client.put('/user',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_delete(self, client, init_database):
        token = create_token()        
        res = client.delete('/order/1',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        resdel = client.delete('/user',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(resdel.data)
        assert resdel.status_code == 200


    def test_client_get_by_jwt(self, client, init_database):
        token = create_token()
        res = client.get('/user/list',
                         headers={'Authorization': 'Bearer ' + token},
                         content_type = 'application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
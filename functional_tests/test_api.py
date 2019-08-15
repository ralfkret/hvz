import unittest
import json
import requests
from retry.api import retry_call
from manged_container import start_container




class ApiFunctionalTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.api_server = start_container('hvz-api', ports={8000:8000})
        retry_call(requests.get, ['http://localhost:8000'], tries=5, delay=0.5, backoff=2, logger=None)
    
    @classmethod
    def tearDownClass(cls):
        cls.api_server.container.remove(force=True)
        pass
    
    def setUp(self):
        pass

    def test_can_get_all_products_without_error(self):
        r = requests.get('http://localhost:8000/hvz/api/v1.0/products')
        assert r.ok

    def test_can_add_a_product(self):
        data={'name':'coffee', 'wanted_amount': 400} 
        r = requests.post('http://localhost:8000/hvz/api/v1.0/products', json=data)
        assert r.ok
        print(r.json())

if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True)
import json
import os
import unittest
from http import HTTPStatus
from types import SimpleNamespace

import docker
import psycopg2
import requests
from retry.api import retry_call

from manged_container import (build_api_container, create_sql_schema,
                              start_container, wait_for_psql_container_ready)

api_url = 'http://localhost:8000/hvz/api/v1.0'


class ApiFunctionalTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        build_api_container()

        db_script_path = os.path.abspath('database/sql_scripts/')
        
        volumes = {db_script_path: {'bind': '/mnt/sql_scripts', 'mode': 'rw'}}
        cls.psql_server = start_container(
            'postgres', publish_all_ports=True, volumes=volumes)
        wait_for_psql_container_ready(cls.psql_server.ip_address)

        create_sql_schema(cls.psql_server.container)

        api_environment = {
            'hvz_api_dbhost':cls.psql_server.ip_address
        }

        cls.api_server = start_container(
            'hvz-api', publish_all_ports=True, environment=api_environment)
        api_server_port = cls.api_server.container.ports['8000/tcp'][0]["HostPort"]

        global api_url 
        api_url = f'http://localhost:{api_server_port}/hvz/api/v1.0'
        retry_call(requests.get, [api_url], tries=5,
                   delay=0.5, backoff=2, logger=None)
        cls.errors_occured = False


    @classmethod
    def tearDownClass(cls):
        api_logs = cls.api_server.container.logs()
        sql_logs = cls.psql_server.container.logs()
        cls.api_server.container.remove(force=True)
        cls.psql_server.container.remove(force=True)
        if cls.errors_occured:
            print('#### LOG OF SQL CONTAINER #####')
            for l in sql_logs.decode('utf-8').split('\n'):
                print('## SQL LOG ## ', l)
            print('#### LOG OF API CONTAINER #####')
            for l in api_logs.decode('utf-8').split('\n'):
                print('## API LOG ## ', l)


    def setUp(self):
        pass


    def get_testrun_errors(self):
        """
        copied from 
            https://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method#39606065
        """
        def list2reason(exc_list):
            if exc_list and exc_list[-1][0] is self:
                return exc_list[-1][1]

        result = self.defaultTestResult()  # these 2 methods have no side effects
        self._feedErrorsToResult(result, self._outcome.errors)
        error = list2reason(result.errors)
        failure = list2reason(result.failures)
        return error or failure


    def tearDown(self):
        self.__class__.errors_occured = self.__class__.errors_occured or self.get_testrun_errors()


    def test_can_get_all_products_without_error(self):
        r = requests.get(f'{api_url}/products')
        assert r.ok


    def test_can_get_a_single_product(self):
        r = requests.get(f'{api_url}/products')
        product = SimpleNamespace(**r.json()[0])
        r1 = requests.get(f'{api_url}/products/{product.id}')
        assert r1.status_code == HTTPStatus.OK
        response_data = SimpleNamespace(**r1.json())
        assert product == response_data


    def test_getting_a_non_existent_product_will_return_404_status(self):
        r = requests.get(f'{api_url}/products/-5')
        assert r.status_code == HTTPStatus.NOT_FOUND


    def test_can_add_a_product(self):
        data = SimpleNamespace(name='coffee', wanted_amount=400)

        r = requests.post(f'{api_url}/products', json=data.__dict__)

        assert r.status_code == HTTPStatus.CREATED
        response_data = SimpleNamespace(**r.json())
        assert response_data.id
        assert response_data.name == data.name
        assert response_data.wanted_amount == data.wanted_amount
        assert r.headers['location'] == f'{api_url}/products/{response_data.id}'
    

    def test_add_product_with_duplicate_name_results_in_409_status(self):
        data = SimpleNamespace(name='Tea', wanted_amount=10)
        r = requests.post(f'{api_url}/products', json=data.__dict__)
        assert r.status_code == HTTPStatus.CREATED

        r = requests.post(f'{api_url}/products', json=data.__dict__)
        assert r.status_code == HTTPStatus.CONFLICT
        response_data = SimpleNamespace(**r.json())

        assert response_data.error
        assert response_data.error == 'Product by the same name already exists.', response_data.error


    def test_can_delete_a_product(self):
        r = requests.get(f'{api_url}/products')
        product = SimpleNamespace(**r.json()[0])
        r1 = requests.delete(f'{api_url}/products/{product.id}')

        assert r1.status_code == HTTPStatus.NO_CONTENT, r1.status_code


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=False)

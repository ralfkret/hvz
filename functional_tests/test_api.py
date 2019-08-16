import unittest
import json
import requests
from http import HTTPStatus
from types import SimpleNamespace
from retry.api import retry_call
from manged_container import start_container

api_url = 'http://localhost:8000/hvz/api/v1.0'


class ApiFunctionalTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_server = start_container('hvz-api', ports={8000: 8000})
        retry_call(requests.get, [api_url], tries=5,
                   delay=0.5, backoff=2, logger=None)
        cls.errors_occured = False


    @classmethod
    def tearDownClass(cls):
        logs = cls.api_server.container.logs()
        cls.api_server.container.remove(force=True)
        if cls.errors_occured:
            print('#### LOG OF API CONTAINER #####')
            for l in logs.decode('utf-8').split('\n'):
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
        assert r.headers['location'] == f'{api_url}/products/{      response_data.id}'
    

    def test_add_product_with_duplicate_name_results_in_409_status(self):
        data = SimpleNamespace(name='Tea', wanted_amount=10)
        r = requests.post(f'{api_url}/products', json=data.__dict__)
        assert r.status_code == HTTPStatus.CREATED

        r = requests.post(f'{api_url}/products', json=data.__dict__)
        assert r.status_code == HTTPStatus.CONFLICT
        response_data = SimpleNamespace(**r.json())

        assert response_data.error
        assert response_data.error == 'Product by the same name already exists.'


    def test_can_delete_a_product(self):
        r = requests.get(f'{api_url}/products')
        product = SimpleNamespace(**r.json()[0])
        r1 = requests.delete(f'{api_url}/products/{product.id}')

        assert r1.status_code == HTTPStatus.NO_CONTENT


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=False)

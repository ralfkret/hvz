import os
import time
import unittest

import psycopg2
from psycopg2.extras import NamedTupleCursor

from context import repository

config = dict(dbname='postgres', user='postgres', host='localhost')

Repository = repository.Repository

class Test_Repository(unittest.TestCase):

    def new_product_name(self):
        return f'product_{time.time()}'

    def reset_db(self):
        with psycopg2.connect(**config) as cn:
            with cn.cursor() as cur:
                sql_script = os.path.join(os.path.dirname(__file__), '../database/sql_scripts/create.sql')
                with open(sql_script, 'r') as f:
                    cur.execute(f.read())
                sql = """
                    insert into
                    product(name, wanted_amount)
                    values 
                        ('milk', 1), 
                        ('honey', 2), 
                        ('sugar', 3), 
                        ('mustard', 4);
                """
                cur.execute(sql)

    def setUp(self):
        self.reset_db()

    def test_repo_throws_if_not_used_as_context_manager(self):
        r = Repository(**config)
        expected_msg = 'Repository::__enter__ not called. You should use the Repository in a with statement.'
        methods = [r.update_product, r.insert_product, r.delete_product, r.get_all_products]
        for m in methods:
            with self.assertRaises(RuntimeError) as cm:
                m()
            assert cm.exception.args[0] == expected_msg, m

    def test_get_all_products(self):
        with Repository(**config) as repo:
            ps = repo.get_all_products()
            name, wanted_amount = ps[0].name, ps[0].wanted_amount
            assert name == 'honey', name
            assert wanted_amount == 2
        

    def test_get_one_product(self):
        with Repository(**config) as repo:
            ps = repo.get_all_products()
            id = ps[0].id
            p = repo.get_one_product(id)
            assert p.name == 'honey'
            assert p.wanted_amount == 2

    def test_get_none_existent_product_returns_None(self):
        with Repository(**config) as repo:
            p = repo.get_one_product(-1)
            assert p == None

    def test_insert_product(self):
        with Repository(**config) as repo:
            name = self.new_product_name()
            p = repo.insert_product(name=name, wanted_amount=55)
            p1 = repo.get_one_product(p.id)
            assert p == p1

    def test_update_product(self):
        with Repository(**config) as repo:
            ps = repo.get_all_products()
            p = ps[0]
            id, name, wanted_amount = p.id, self.new_product_name(), p.wanted_amount+10
            d = dict(name=name, wanted_amount=wanted_amount)
            success = repo.update_product(id, **d)
            assert success

        with Repository(**config) as repo:
            p1 = repo.get_one_product(p.id)
            assert id == p1.id
            assert name == p1.name
            assert wanted_amount == p1.wanted_amount

    def test_update_of_non_existent_product_returns_None(self):
        with Repository(**config) as repo:
            id, name, wanted_amount = -1, 'something', -1
            d = dict(name=name, wanted_amount=wanted_amount)
            success = repo.update_product(id, **d)
            assert not success

    def test_delete_product(self):
        with Repository(**config) as repo:
            ps = repo.get_all_products()
            id = ps[0].id
            success = repo.delete_product(id)
            assert success

    def test_delete_of_non_existent_product_returns_None(self):
        with Repository(**config) as repo:
            success = repo.delete_product(-1)
            assert not success

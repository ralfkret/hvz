import unittest
import manged_container
import psycopg2 as dbapi2
from retry.api import retry_call


class FunctionalTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.psql_server = manged_container.start_container('postgres')
        args = {'user':'postgres', 'host':cls.psql_server.ip_address}
        cls._connection = retry_call(dbapi2.connect, fkwargs=args , tries=5, delay=0.5, logger=None)
    
    @property
    def db_connection(self):
        return self.__class__._connection

    @classmethod
    def tearDownClass(cls):
        cls.psql_server.container.remove(force=True)
    
    def setUp(self):
        with open('./database/sql_scripts/create.sql', 'r') as f:
            sql = f.read()
        cur = self.db_connection.cursor()
        cur.execute(sql)
        self.db_connection.commit()
        cur.close()

    def test_table_products_exist(self):
        cur = self.db_connection.cursor()
        cur.execute('SELECT * FROM product')
        cur.fetchall()

    def test_table_stock_movement_exist(self):
        cur = self.db_connection.cursor()
        cur.execute('SELECT * FROM stock_movement')
        cur.fetchall()


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True)
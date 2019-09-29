#!/usr/bin/env python3

import unittest
import psycopg2

class DBTest(unittest.TestCase):
  def setUp(self):
    self.conn = psycopg2.connect("dbname='hvs' user='postgres' host='localhost' password='a3FJrSJ7'")
    self.conn.autocommit = True
    cur = self.conn.cursor()

    sql_file = open("create.sql")
    cur.execute(sql_file.read())
    sql_file.close()

    data_file = open("test_data.sql")
    cur.execute(data_file.read())
    data_file.close()

  def tearDown(self):
    self.conn.close()

  def test_data_product(self):
    cur = self.conn.cursor()
    cur.execute("SELECT name, wanted_amount FROM product;")
    self.assertEqual(cur.rowcount, 3)
    self.assertEqual(cur.fetchone(), ("water", 3))
    self.assertEqual(cur.fetchone(), ("bread", 1))
    self.assertEqual(cur.fetchone(), ("apple", 5))

  def test_data_stock_movement(self):
    cur = self.conn.cursor()
    cur.execute("SELECT amount FROM stock_movement;")
    self.assertEqual(cur.rowcount, 3)
    self.assertEqual(cur.fetchone(), (3,))
    self.assertEqual(cur.fetchone(), (9,))
    self.assertEqual(cur.fetchone(), (-3,))

  def test_total_amount_products(self):
    cur = self.conn.cursor()
    cur.execute("SELECT name, wanted_amount, total, missing FROM total_amount_product;")
    self.assertEqual(cur.rowcount, 3)
    self.assertEqual(cur.fetchone(), ("bread", 1, 0, 1))
    self.assertEqual(cur.fetchone(), ("apple", 5, 6, -1))
    self.assertEqual(cur.fetchone(), ("water", 3, 3, 0))

  def test_no_negative_amount_trigger(self):
    cur = self.conn.cursor()

    cur.execute("""INSERT INTO hvs.stock_movement (amount, product_id)
    SELECT -1, id FROM hvs.product WHERE name = 'apple';""")

    with self.assertRaises(psycopg2.errors.RaiseException):
      tmp_cur = self.conn.cursor()
      tmp_cur.execute("""INSERT INTO hvs.stock_movement (amount, product_id)
      SELECT 0, id FROM hvs.product WHERE name = 'water';""")

    with self.assertRaises(psycopg2.errors.RaiseException):
      tmp_cur = self.conn.cursor()
      tmp_cur.execute("""INSERT INTO hvs.stock_movement (amount, product_id)
      SELECT -1, id FROM hvs.product WHERE name = 'bread';""")

if __name__ == "__main__":
  unittest.main()

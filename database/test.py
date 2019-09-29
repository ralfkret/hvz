#!/usr/bin/env python3

import psycopg2

def main():
  conn = psycopg2.connect("dbname=hvs user=postgres")
  cur = conn.cursor()
  cur.execute("SELECT * FROM product;")
  print(cur.fetchone())

if __name__ == "__main__":
  main()

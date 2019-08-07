-- Dropping everything

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Creation of tables

CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  wanted_amount INTEGER NOT NULL
);

CREATE TABLE stock_movement (
  id SERIAL PRIMARY KEY,
  amount INTEGER NOT NULL,
  product_id INTEGER NOT NULL REFERENCES product (id)
);


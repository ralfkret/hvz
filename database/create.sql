-- Dropping everything

DROP SCHEMA IF EXISTS hvs CASCADE;
CREATE SCHEMA hvs;

DROP FUNCTION IF EXISTS no_negative_amount_function;

DROP TRIGGER IF EXISTS no_negative_amount_trigger 
ON hvs.stock_movement CASCADE;

-- Setting the standart schema

SET search_path TO hvs;

-- Creation of tables

CREATE TABLE hvs.product (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  wanted_amount INTEGER NOT NULL
);

CREATE TABLE hvs.stock_movement (
  id SERIAL PRIMARY KEY,
  amount INTEGER NOT NULL,
  product_id INTEGER NOT NULL REFERENCES hvs.product (id)
);

-- Creation of views

CREATE VIEW total_amount_product AS
SELECT product.id, name, wanted_amount, coalesce(sum(amount), 0) as total, wanted_amount - coalesce(sum(amount), 0) as missing
FROM hvs.stock_movement
RIGHT JOIN hvs.product
on product.id = product_id
GROUP BY product.id, name, wanted_amount;

-- Creation of triggers

CREATE FUNCTION no_negative_amount_function()
RETURNS trigger AS $no_negative_amount_function$
BEGIN
  IF NEW.amount = 0 THEN
    RAISE EXCEPTION 'The amount of a product can not be 0';
  END IF;
  IF (NEW.amount + total < 0) FROM hvs.total_amount_product WHERE id = NEW.product_id THEN
    RAISE EXCEPTION 'The amount of a product can not be less than 0';
  END IF;
  RETURN NEW;
END;
$no_negative_amount_function$ LANGUAGE 'plpgsql';

CREATE TRIGGER no_negative_amount_trigger
BEFORE INSERT ON hvs.stock_movement FOR ROW
EXECUTE PROCEDURE no_negative_amount_function();

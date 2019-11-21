INSERT INTO hvs.product (name, wanted_amount) VALUES
('water', 3), ('bread', 1), ('apple', 5);

INSERT INTO hvs.stock_movement (amount, product_id)
SELECT 3, id FROM hvs.product WHERE name = 'water';

INSERT INTO hvs.stock_movement (amount, product_id)
SELECT 9, id FROM hvs.product WHERE name = 'apple';

INSERT INTO hvs.stock_movement (amount, product_id)
SELECT -3, id FROM hvs.product WHERE name = 'apple';

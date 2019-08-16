-- This file is best used with the VS Code extension SQLTools (https://vscode-sqltools.mteixeira.dev/)


-- @block select products
select
  *
from
  product; 

-- @block delete all 
delete from
  stock_movement;
delete from
  product;


-- @block insert some product
insert into
  product(name, wanted_amount)
values 
('milk', 1), 
('honey', 2), 
('sugar', 3), 
('mustard', 4)


-- @block inset some stock_movement
insert into stock_movement(amount, product_id)
values 
  (10, (select id from product where name = 'milk')),
  (20, (select id from product where name = 'honey')),
  (30, (select id from product where name = 'sugar'))


-- @block query product_stock
select * from product_stock
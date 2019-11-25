import pytest
import sqlalchemy


def test_product_list(dbexecutor):
    rows = dbexecutor('select * from hvs.product;')
    assert len(rows) == 3


def test_data_product(dbexecutor):
    rows = dbexecutor("SELECT name, wanted_amount FROM product ORDER BY name DESC;")
    assert len(rows) == 3
    assert rows[0] == ("water", 3)
    assert rows[1] == ("bread", 1)
    assert rows[2] == ("apple", 5)

def test_data_stock_movement(dbexecutor):
    rows = dbexecutor("SELECT amount FROM stock_movement ORDER BY id;")
    assert len(rows) == 3
    assert rows[0] == (3,)
    assert rows[1] == (9,)
    assert rows[2] == (-3,)

def test_total_amount_products(dbexecutor):
    rows = dbexecutor("SELECT name, wanted_amount, total, missing FROM total_amount_product ORDER BY id;")
    assert len(rows) == 3
    assert rows[0] == ("water", 3, 3, 0)
    assert rows[1] == ("bread", 1, 0, 1)
    assert rows[2] == ("apple", 5, 6, -1)

def test_no_negative_amount_trigger(dbexecutor):
    dbexecutor("INSERT INTO hvs.stock_movement (amount, product_id) "
        "SELECT -1, id FROM hvs.product WHERE name = 'apple';")

    with pytest.raises(  sqlalchemy.exc.InternalError):
        dbexecutor("INSERT INTO hvs.stock_movement (amount, product_id) "
            "SELECT 0, id FROM hvs.product WHERE name = 'water';")

    with pytest.raises(  sqlalchemy.exc.InternalError):
        dbexecutor("INSERT INTO hvs.stock_movement (amount, product_id) "
            "SELECT -1, id FROM hvs.product WHERE name = 'bread';")

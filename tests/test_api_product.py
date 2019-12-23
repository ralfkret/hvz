from web.models import Product


def product_url(id):
    return f'/api/v1/product/{id}'


def test_get_one_product(client):
    result = client.get(product_url(1)).get_json()
    assert result['name'] == 'water'


def test_non_existant_product_returns_404_and_json_error_msg(client):
    result = client.get(product_url(-1), headers={'ACCEPT': 'application/json'})
    assert result.status_code == 404
    d = result.get_json()
    assert d['error'] == 'not found'


def test_modify_product_just_change_name(client):
    new_name = 'Sparkling water'
    result = client.put(product_url(1), json={'name': new_name})
    assert result.status_code == 200
    p = Product.query.get(1)
    assert p.name == new_name


def test_modify_product_just_change_wanted_amount(client):
    new_wanted_amount = 5555
    result = client.put(product_url(1), json={
                        'wanted_amount': new_wanted_amount})
    assert result.status_code == 200
    p = Product.query.get(1)
    assert p.wanted_amount == new_wanted_amount


def test_modify_product_change_name_and_wanted_amount(client):
    new_name = 'Sparkling water'
    new_wanted_amount = 5555
    result = client.put(product_url(1), json={'name': new_name,
                                              'wanted_amount': new_wanted_amount})
    assert result.status_code == 200
    p = Product.query.get(1)
    assert p.wanted_amount == new_wanted_amount
    assert p.name == new_name


def test_delete_product(client):
    result = client.delete(product_url(2))
    assert result.status_code == 204


def test_delete_product_with_stock_movements_returns_error(client):
    result = client.delete(product_url(1))
    assert result.status_code == 412
    assert result.get_json()['error'] == 'Can\'t delete product with stock_movements'
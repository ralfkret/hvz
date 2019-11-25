from web import create_app


def test_config():
    assert not create_app().testing
    assert create_app('testing').testing


def test_landing_page(client):
    response = client.get('/', follow_redirects=True)
    assert b'Produkte' in response.data

def test_product_list(client):
    response = client.get('/', follow_redirects=True)
    assert b'water' in response.data
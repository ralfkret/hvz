from web import db
from web.models import Product

from urllib.parse import urlencode, urljoin


def products_url(**kwargs):
    return '/api/v1/products?' + urlencode(kwargs)


def test_products_paging(client):
    url = products_url(page=1, per_page=1)
    r = client.get(url)
    json = r.get_json()
    assert 'products' in json
    assert len(json['products']) == 1
    assert not json['prev']
    assert json['next']
    assert json['count'] == 3
    assert json['pages'] == [1, 2, 3]


def test_products_paging_with_90_products(client):
    for i in range(3, 100):
        db.session.add(Product(name=f'Product-{i}', wanted_amount=i))
    db.session.commit()
    json = client.get(products_url(page=1, per_page=10)).get_json()
    assert len(json['products']) == 10
    assert json['count'] == 100
    assert json['pages'] == [1, 2, None, 10]


def test_products_paging_with_90_products_page_3(client):
    for i in range(3, 100):
        db.session.add(Product(name=f'Product-{i}', wanted_amount=i))
    db.session.commit()
    json = client.get(products_url(page=3, per_page=10)).get_json()
    assert len(json['products']) == 10
    assert json['next']
    assert json['prev']
    assert json['count'] == 100
    assert json['pages'] == [1, 2, 3, 4, None, 10]

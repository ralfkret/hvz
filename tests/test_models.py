from web.models import Product, StockMovement
from web import db

def test_product_model(app):
    products = Product.query.order_by(Product.id).all()
    assert len(products) == 3


def test_create_product(app):
    db.session.add(Product(name='new', wanted_amount=5))
    db.session.commit()
    products = Product.query.order_by(Product.id).all()
    assert len(products) == 4


def test_stockmovement_model(app):
    stock_movements = StockMovement.query.all()
    assert len(stock_movements) == 3


def test_relationsship_product_to_stockmovement(app):
    apple = Product.query.filter_by(name='apple').first()
    stock_movements = apple.stock_movements.all()
    assert len(stock_movements) == 2


def test_relationsship_product_to_stock_movement_is_lazy(app):
    apple = Product.query.filter_by(name='apple').first()
    sms = apple.stock_movements.order_by('id')
    assert sms[0].id == 2


def test_relationship_stock_movement_to_product(app):
    sm = StockMovement.query.filter_by(product_id = 3).first()
    assert sm.product.name == 'apple'

def test_joins(app):
    sms = StockMovement.query.join(StockMovement.product).filter_by(name='apple').all()
    assert len(sms) == 2
from flask import url_for
from . import db


class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'schema': 'hvs'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True)
    wanted_amount = db.Column(db.Integer, nullable=False)
    stock_movements = db.relationship('StockMovement', backref='product', lazy='dynamic')

    def to_json(self):
        json_product = {
            'url': url_for('api.get_product', id=self.id),
            'name': self.name,
            'wanted_amount': self.wanted_amount,
            'stock_movement_count': self.stock_movements.count()
        }
        return json_product


    def __repr__(self):
        return f'Product(id={self.id}, name=\'{self.name}\', wanted_amount={self.wanted_amount})'

class StockMovement(db.Model):
    __tablename__ = 'stock_movement'
    __table_args__ = {'schema': 'hvs'}

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('hvs.product.id'))

    def __repr__(self):
        return f'StockMovement(id={self.id}, amount=\'{self.amount}\', product_id={self.product_id})'
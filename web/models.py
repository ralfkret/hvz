from . import db

StockMovement=None


class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'schema': 'hvs'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True)
    wanted_amount = db.Column(db.Integer)

    def __repr__(self):
        return f'Product(id={self.id}, name=\'{self.name}\', wanted_amount={self.wanted_amount})'
from flask import Flask, jsonify, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    wanted_amount = db.Column(db.Integer, nullable=False)

    def to_json(self):
      return {
        'id': self.id,
        'name': self.name,
        'wanted_amount': self.wanted_amount,
      }

    @staticmethod    
    def from_json(json_post):        
      name = json_post.get('name')        
      wanted_amount = json_post.get('wanted_amount')        
      return Product(name=name, wanted_amount=wanted_amount)

db.drop_all()
db.create_all()

products = [
  { "id": 1, "name": "Artichokes - Knobless, White", "wanted_amount": 19 }, 
  { "id": 2, "name": "Cabbage - Nappa", "wanted_amount": 70 }, 
  { "id": 3, "name": "Sausage - Meat", "wanted_amount": 24 }, 
  { "id": 4, "name": "Tomatoes - Roma", "wanted_amount": 47 }
]

for p in products:
  db.session.add(Product(name = p['name'], wanted_amount = p['wanted_amount']))
db.session.commit()

@app.route('/hvz/api/v1.0/products', methods=['GET'])
def get_products():
    return jsonify([p.to_json() for p in Product.query.all()])

@app.route('/hvz/api/v1.0/products/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify(Product.query.get_or_404(id).to_json())

@app.route('/hvz/api/v1.0/products/', methods=['POST'])
def new_product():    
  p = Product.from_json(request.json)    
  db.session.add(p)    
  db.session.commit()    
  return jsonify(p.to_json()), 201, {'Location': url_for('get_product', id=p.id)}

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port= 81)
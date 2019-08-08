from flask import Flask, jsonify, make_response

app = Flask(__name__)



products = [{
  "id": 1,
  "name": "Artichokes - Knobless, White",
  "wanted_amount": 19
}, {
  "id": 2,
  "name": "Cabbage - Nappa",
  "wanted_amount": 70
}, {
  "id": 3,
  "name": "Sausage - Meat",
  "wanted_amount": 24
}, {
  "id": 4,
  "name": "Tomatoes - Roma",
  "wanted_amount": 47
}]

@app.route('/hvz/api/v1.0/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

print("a")
if __name__ == "__main__":
  app.run(host='0.0.0.0', port= 81)
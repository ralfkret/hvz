from . import api
from ..models import Product
from flask import request, current_app, url_for, jsonify


@api.route('product/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_json())


@api.route('products')
def get_products():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.paginate( page, per_page=5, error_out=False)
    products = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_products', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_products', page=page+1)
    return jsonify({
        'products': [p.to_json() for p in products],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
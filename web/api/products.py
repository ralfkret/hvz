from flask import current_app, jsonify, make_response, request, url_for

from web import db

from ..models import Product
from . import api


def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']

    return response


@api.route('product/<int:id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def get_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'PUT':
        if 'name' in request.json:
            product.name = request.json['name']
        if 'wanted_amount' in request.json:
            product.wanted_amount = request.json['wanted_amount']
        db.session.add(product)
        db.session.commit()
    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify_no_content()
    return jsonify(product.to_json())


@api.route('products')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    pagination = Product.query.paginate(
        page, per_page=per_page, error_out=False)
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
        'count': pagination.total,
        'pages': [i for i in pagination.iter_pages(left_edge=1, left_current=1, right_current=2, right_edge=1)]
    })

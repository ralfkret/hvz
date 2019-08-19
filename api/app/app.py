from flask import Flask, jsonify, make_response, request, url_for
import logging
from repository import Repository
import psycopg2
from http import HTTPStatus
from types import SimpleNamespace
from os import getenv

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

config = SimpleNamespace(
    db = SimpleNamespace(
        dbname=getenv('hvz_api_dbname', 'postgres'),
        user=getenv('hvz_api_dbuser', 'postgres'),
        password=getenv('hvz_api_dbpassword', ''),
        host=getenv('hvz_api_dbhost', 'localhost'),
        port=getenv('hvz_api_dbport', '5432'),
        ), 
    api = SimpleNamespace(
        host=getenv('hvz_api_listen_ip_address', '0.0.0.0'),
        port=getenv('hvz_api_listen_ip_port', '8000'), 
        )
    )

logging.debug(f'starting api with config: {config}')

def repo():
    return Repository(**config.db.__dict__)


@app.route('/hvz/api/v1.0/products', methods=['GET'])
def get_products():
    with repo() as r:
        return jsonify([p._asdict() for p in r.get_all_products()])


@app.route('/hvz/api/v1.0/products/<int:id>', methods=['GET'])
def get_product(id):
    with repo() as r:
        p = r.get_one_product(id)
        if p:
            return jsonify(r.get_one_product(id)._asdict())
        else:
            return jsonify({'error': 'Product not found.'}), HTTPStatus.NOT_FOUND


@app.route('/hvz/api/v1.0/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    with repo() as r:
        success = r.delete_product(id)
        if success:
            return '', HTTPStatus.NO_CONTENT
        else:
            return jsonify({'error': 'Product not found.'}), HTTPStatus.NOT_FOUND


@app.route('/hvz/api/v1.0/products/', methods=['POST'])
def new_product():
    with repo() as r:
        try:
            p = r.insert_product(**request.json)
            return jsonify(p._asdict()), HTTPStatus.CREATED, {'Location': url_for('get_product', id=p.id)}
        except psycopg2.errors.Error as e: #pylint: disable=E1101
            return jsonify({'error': 'Product by the same name already exists.'}), HTTPStatus.CONFLICT
        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    app.run(**config.api.__dict__)
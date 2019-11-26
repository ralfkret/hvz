import os
import tempfile

import pytest
from web import create_app, db
from app import execute_sql

def _get_sql(filename):
    with open(os.path.join(os.path.dirname(__file__), '..', 'database', filename), 'rb') as f:
        return f.read().decode('utf8')

_create_sql = _get_sql('create.sql')
_data_sql = _get_sql('test_data.sql')


@pytest.fixture
def dbexecutor(app):
    with app.app_context():
        yield execute_sql

@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        execute_sql(_create_sql)
        execute_sql(_data_sql)

        yield app


@pytest.fixture
def client(app):
    return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()
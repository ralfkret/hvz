import os
import click
from logging import getLogger
from web import create_app, db
from web.models import Product, StockMovement

logger = getLogger(__name__)
logger.info('creating app')
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

basedir = os.path.abspath(os.path.dirname(__file__))

def get_all_products():
    return Product.query.all()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Product=Product, gap=get_all_products)


@app.cli.command()
def create_database():
    with open(os.path.join(basedir, 'database', 'create.sql')) as f:
        sql = f.read()
        cn = db.engine.connect()
        t = cn.begin()
        cn.execute(sql)
        t.commit()
        cn.close()
        
    
@app.cli.command()
def add_test_data():
    with open(os.path.join(basedir, 'database', 'test_data.sql')) as f:
        sql = f.read()
        cn = db.engine.connect()
        t = cn.begin()
        cn.execute(sql)
        t.commit()
        cn.close()


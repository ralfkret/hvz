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


def execute_sql(sql):
    with db.engine.connect() as cn:
        with cn.begin() as txn:
            result = cn.execute(sql)
            rows = None
            if result.returns_rows:
                rows = result.fetchall()
            txn.commit()
        cn.close()
    return rows


@app.cli.command()
def create_database():
    with open(os.path.join(basedir, 'database', 'create.sql')) as f:
        sql = f.read()
        execute_sql(sql)
        
 
@app.cli.command()
def add_test_data():
    with open(os.path.join(basedir, 'database', 'test_data.sql')) as f:
        sql = f.read()
        execute_sql(sql)
 

@app.cli.command()
def add_1000_products():
    with open(os.path.join(basedir, 'database', 'products-1000.sql')) as f:
        lines = f.read().split('\n')
        for sql in lines:
            try:
                execute_sql(sql) 
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logger.error(e)
                pass



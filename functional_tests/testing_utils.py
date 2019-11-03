import os
import time
import psycopg2


def new_product_name():
    """
    Create a new product name that is unique
    """
    return f'product_{time.time()}'

def reset_db(**kwargs):
    """
    Reset the database by executing the create sql script.
    Args:
        config - mapping of connection parameters.
        sql - extra sql to execute. Typically some test data. 
    """
    with psycopg2.connect() as cn:
        with cn.cursor() as cur:
            sql_script = os.path.join(os.path.dirname(__file__), '../database/sql_scripts/create.sql')
            with open(sql_script, 'r') as f:
                cur.execute(f.read())
            sql = """
                insert into
                product(name, wanted_amount)
                values 
                    ('milk', 1), 
                    ('honey', 2), 
                    ('sugar', 3), 
                    ('mustard', 4);
            """
            cur.execute(sql)
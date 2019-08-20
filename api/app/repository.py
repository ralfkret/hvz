import psycopg2
from psycopg2.extras import NamedTupleCursor
from functools import wraps

class Repository():
    """
    Functions to access the PostgreSQL Database for hvz. 
    Any exceptions thrown by the database will be passed to the caller.
    """

    def __init__(self, **kwargs):
        # http://initd.org/psycopg/docs/usage.html#basic-module-usage
        # http://initd.org/psycopg/docs/extras.html?highlight=namedtuplecursor#namedtuple-cursor
        self.connection = psycopg2.connect(
            cursor_factory=NamedTupleCursor, **kwargs)
        self.cursor = None

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.cursor = None
        self.connection.commit()
        self.connection.close()

    def guard(f): #pylint: disable=no-self-argument
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            if not self.cursor:
                raise RuntimeError(
                    'Repository::__enter__ not called. You should use the Repository in a with statement.')
            return f(self, *args, **kwargs) #pylint: disable=not-callable
        return wrapped

    @guard
    def get_all_products(self):
        """
        Get a list of all products.
        The list will be sorted by the product name.
        """
        self.cursor.execute(
            'select id, name, wanted_amount from product order by name;')
        return list(self.cursor.fetchall())

    @guard
    def get_one_product(self, id):
        """ 
        Return the product as specified by the id as a namedtuple or None if the product does not exist.
        """
        self.cursor.execute(
            'select id, name, wanted_amount from product where id = %s', (id, ))
        return self.cursor.fetchone()

    @guard
    def insert_product(self, **kwargs):
        """
        Insert a new product into the database. Pass the column values as kwargs.
        Return the created product as a namedtuple.
        """
        self.cursor.execute('''
            insert into product (name, wanted_amount) 
            values (%(name)s, %(wanted_amount)s) returning id;''', kwargs)
        id = self.cursor.fetchone()
        return self.get_one_product(id)

    @guard
    def update_product(self, id, **kwargs):
        """
        Update the product specified by the id. Pass the colum values as kwargs.
        Return True if the update is successfull, return False if no product with
        the given id exists.
        """
        kwargs['id'] = id
        self.cursor.execute('''
        update product set
            name = %(name)s, wanted_amount = %(wanted_amount)s
        where id = %(id)s
        ''', kwargs)
        return self.cursor.rowcount > 0

    @guard
    def delete_product(self, id):
        """
        Delete the product specified by the id. 
        Return True if the delete is successfull, return False if no product with
        the given id exists.
        """
        self.cursor.execute('delete from product where id = %s', (id, ))
        return self.cursor.rowcount > 0

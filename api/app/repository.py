import psycopg2
from psycopg2.extras import NamedTupleCursor


def __reset_db_for_doctest():
    with psycopg2.connect(dbname='postgres', user='postgres', host='localhost') as cn:
        with cn.cursor() as cur:
            cur.execute('delete from stock_movement;')
            cur.execute('delete from product;')
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

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def get_all_products(self):
        """
        Get a list of all products.
        The list will be sorted by the product name.

        >>> __reset_db_for_doctest()
        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     ps = repo.get_all_products()
        ...     name, wanted_amount = ps[0].name, ps[0].wanted_amount
        ...     assert name == 'honey', name
        ...     assert wanted_amount == 2
        """
        self.cursor.execute(
            'select id, name, wanted_amount from product order by name;')
        return list(self.cursor.fetchall())

    def get_one_product(self, id):
        """ 
        Return the product as specified by the id as a namedtuple or None if the product does not exist.

        >>> __reset_db_for_doctest()
        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     ps = repo.get_all_products()
        ...     id = ps[0].id
        ...     p = repo.get_one_product(id)
        ...     assert p.name == 'honey'
        ...     assert p.wanted_amount == 2

        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     p = repo.get_one_product(-1)
        ...     assert p == None
        """
        self.cursor.execute(
            'select id, name, wanted_amount from product where id = %s', (id, ))
        return self.cursor.fetchone()

    def insert_product(self, **kwargs):
        """
        Insert a new product into the database. Pass the column values as kwargs.
        Return the created product as a namedtuple.
        >>> import time
        >>> __reset_db_for_doctest()
        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     name = str(time.time())
        ...     p = repo.insert_product(name=name, wanted_amount=55)
        ...     p1 = repo.get_one_product(p.id)
        ...     assert p == p1
        """
        self.cursor.execute('''
            insert into product (name, wanted_amount) 
            values (%(name)s, %(wanted_amount)s) returning id;''', kwargs)
        id = self.cursor.fetchone()
        return self.get_one_product(id)

    def update_product(self, id, **kwargs):
        """
        Update the product specified by the id. Pass the colum values as kwargs.
        Return True if the update is successfull, return False if no product with
        the given id exists.
        >>> import time
        >>> __reset_db_for_doctest()
        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     ps = repo.get_all_products()
        ...     p = ps[0]
        ...     id, name, wanted_amount = p.id, str(time.time()), p.wanted_amount+10
        ...     d = dict(name=name, wanted_amount=wanted_amount)
        ...     success = repo.update_product(id, **d)
        ...     assert success

        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     p1 = repo.get_one_product(p.id)
        ...     assert id == p1.id
        ...     assert name == p1.name
        ...     assert wanted_amount == p1.wanted_amount

        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     id, name, wanted_amount = -1, 'something', -1
        ...     d = dict(name=name, wanted_amount=wanted_amount)
        ...     success = repo.update_product(id, **d)
        ...     assert not success
        """
        kwargs['id'] = id
        self.cursor.execute('''
        update product set
            name = %(name)s, wanted_amount = %(wanted_amount)s
        where id = %(id)s
        ''', kwargs)
        return self.cursor.rowcount > 0

    def delete_product(self, id):
        """
        Delete the product specified by the id. 
        Return True if the delete is successfull, return False if no product with
        the given id exists.
        >>> import time
        >>> __reset_db_for_doctest()
        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     ps = repo.get_all_products()
        ...     id = ps[0].id
        ...     success = repo.delete_product(id)
        ...     assert success

        >>> with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ...     success = repo.delete_product(-1)
        ...     assert not success
        """
        self.cursor.execute('delete from product where id = %s', (id, ))
        return self.cursor.rowcount > 0


if __name__ == "__main__":
    import time
    __reset_db_for_doctest()
    with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        ps = repo.get_all_products()
        p = ps[0]
        id, name, wanted_amount = p.id, str(time.time()), p.wanted_amount+10
        d = dict(name=name, wanted_amount=wanted_amount)
        success = repo.update_product(id, **d)
        assert success
    with Repository(dbname='postgres', user='postgres', host='localhost') as repo:
        p1 = repo.get_one_product(p.id)
        assert id == p1.id
        assert name == p1.name
        assert wanted_amount == p1.wanted_amount

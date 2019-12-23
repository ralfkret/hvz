from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        Numeric, String, ForeignKey, DateTime, ForeignKey,
                        Index, ForeignKeyConstraint, insert)
from datetime import datetime

metadata = MetaData()

cookies = Table('cookies', metadata,
                Column('id', Integer(), primary_key=True),
                Column('name', String(50), index=True, unique=True),
                Column('recipe_url', String(255)),
                Column('sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12, 2))
                )
Index('ix_cookies_sku' 'sku', unique=True)

users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('name', String(15), nullable=False, unique=True),
              Column('email_address', String(255)),
              Column('phone', String(20), nullable=False),
              Column('password', String(25), nullable=False),
              Column('created_on', DateTime(), default=datetime.now),
              Column('updated_on', DateTime(),
                     default=datetime.now, onupdate=datetime.now)
              )

orders = Table('orders', metadata,
               Column('id', Integer(), primary_key=True),
               Column('user_id', Integer(), ForeignKey('users.id'))
               )

line_items = Table('line_items', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('order_id', ForeignKey('orders.id')),
                   Column('cookie_id', ForeignKey('cookies.id')),
                   Column('quantity', Integer()),
                   Column('extended_cost', Numeric(12, 2))
                   )


engine = create_engine('postgres://postgres:@localhost', echo=True)
engine.echo = False

metadata.drop_all(engine)
metadata.create_all(engine)

connection = engine.connect()


ins = cookies.insert().values(
    name='chocolate chip',
    recipe_url='http://example.org',
    sku='CC01',
    quantity=12,
    unit_cost=0.50
)


result = connection.execute(ins)


cookies_list = [
    dict(name='peanut butter',
         recipe_url='http://example.org/peanut+butter',
         sku='pb01',
         quantity='24',
         unit_cost=0.25),
    dict(name='outmeal raisin',
         recipe_url='http://example.org/outmeal+raisin',
         sku='or01',
         quantity=100,
         unit_cost=1.25),
]


result = connection.execute(ins, cookies_list)
print(result.rowcount)

from sqlalchemy import select, desc, text
from pprint import pprint as pp

s = select([cookies])
rp = connection.execute(s)
pp(rp.fetchall())


s = select([cookies.c.name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.name))
rp = connection.execute(s)
pp(rp.keys())
pp(rp.fetchone())
pp(rp.fetchone())
pp(rp.first())


from sqlalchemy import func

s = select([func.sum(cookies.c.quantity), text('\'#\'')])
rp = connection.execute(s)
pp(rp.first())


s = select([func.count(cookies.c.name).label('total_count')])
rp = connection.execute(s)
row = rp.first()
pp(row.keys())
pp(row['total_count'])
pp(row.total_count)


s = select([cookies]).where(cookies.c.name.like('%chip'))
rp = connection.execute(s)
row = rp.first()
pp(row.keys())
pp(row.items())


s = select([cookies.c.name, 'SKU-' + cookies.c.sku])
for row in connection.execute(s):
    print(row)


from sqlalchemy import cast

_cast = cast( cookies.c.quantity * cookies.c.unit_cost, Numeric(12,2))
s = select([cookies.c.name, _cast.label('a'), _cast.label('n')]) 
for row in connection.execute(s):
    print(row)

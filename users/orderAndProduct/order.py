import json
import datetime

from decouple import config
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, insert, update, Boolean, \
    DateTime
from users.orderAndProduct.products import pizzas as Ppizzas
from users.orderAndProduct.products import drinks as Pdrinks

db_connect = config('database-connect-addres')
meta = MetaData()

orders = Table('orders', meta,
               Column('id', Integer(), primary_key=True),
               Column('user', String(), default=None),
               Column('pizzas', String(), default=None),
               Column('drinks', String(), default=None),
               Column('promocode', String(), default=None),
               Column('promocode_item', String(), default=None),

               Column('street', String(255), default=None),
               Column('house', String(255), default=None),
               Column('entrance', String(255), default=None),
               Column('floor', String(255), default=None),
               Column('apartment', String(255), default=None),

               Column('device', String(), default=None),
               Column('paytype', String(), default=None),
               Column('price', Integer(), default=None),
               Column('comment', String(), default=None),
               Column('status', String()),
               # Column('deliver', ForeignKey(deliver.id)),
               Column('data', DateTime())
               )

streets = Table('streets', meta,
                Column('street', String(), default=None),
                Column('is_view', Boolean(), default=True))


def set_order(user, pizzas, drinks, promocode, promocode_item, street, house, entrance, floor, apartment, device,
              paytype, price, comment, status, data):
    ins = orders.insert().values(user=user, pizzas=pizzas, drinks=drinks, promocode=promocode,
                                 promocode_item=promocode_item,
                                 street=street, house=house, entrance=entrance,
                                 floor=floor, apartment=apartment, device=device, paytype=paytype, price=price,
                                 comment=comment, status=status, data=data)
    fin = conn.execute(ins)


def get_order(number):
    sel = select(
        [orders.c.id, orders.c.user, orders.c.pizzas, orders.c.drinks, orders.c.promocode_item, orders.c.street,
         orders.c.house, orders.c.entrance, orders.c.floor, orders.c.apartment, orders.c.paytype,
         orders.c.comment, orders.c.status, orders.c.data]).where(orders.c.user == number)
    res = conn.execute(sel).fetchall()
    result = []
    for i in res:
        result.append({
            "id": i[0],
            "user": i[1],
            "pizzas": json.loads(i[2]),
            "drink": json.loads(i[3]),
            "promocode_item": json.loads(i[4]),
            "street": i[5],
            "house": i[6],
            "entrance": i[7],
            "floor": i[8],
            "apartment": i[9],
            "paytype": i[10],
            "comment": i[11],
            "status": i[12],
            "data": i[13],
        })
    return result


engine = create_engine(db_connect, echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()

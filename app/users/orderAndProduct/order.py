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



def set_order(user, pizzas, drinks, promocode, promocode_item, street, house, entrance, floor, apartment, device,
              paytype, price, comment, status, data):
    ins = orders.insert().values(user=user, pizzas=pizzas, drinks=drinks, promocode=promocode,
                                 promocode_item=promocode_item,
                                 street=street, house=house, entrance=entrance,
                                 floor=floor, apartment=apartment, device=device, paytype=paytype, price=price,
                                 comment=comment, status=status, data=data).returning(
                orders.c.id,
                orders.c.pizzas,
            )
    fin = conn.execute(ins).fetchone()
    return fin[0]


def get_order(id, number):
    sel = select(
        [orders.c.id, orders.c.user, orders.c.pizzas, orders.c.drinks, orders.c.promocode_item, orders.c.street,
         orders.c.house, orders.c.entrance, orders.c.floor, orders.c.apartment, orders.c.paytype, orders.c.price,
         orders.c.comment, orders.c.status, orders.c.data]).where(orders.c.id == id).where(orders.c.user == number)
    res = conn.execute(sel).fetchone()

    # print(res[13])


    if res[13] == "backout" or res[13] == 'completed':
        return {'status': 401, 'message': 'Этот заказ уже доставлен или отменён'}

    # if res[13] == "accepted" or res[13] == "completed" or res[13] == "delivery":
    x = ""
    if res[4] != None:
        # Проверка на наличие промокода
        x = json.loads(res[4])

    result = {
        "id": res[0],
        "user": res[1],
        "pizzas": json.loads(res[2]),
        "drink": json.loads(res[3]),
        "promocode_item": x,
        "street": res[5],
        "house": res[6],
        "entrance": res[7],
        "floor": res[8],
        "apartment": res[9],
        "paytype": res[10],
        "totalprice": res[11],
        "comment": res[12],
        "status": res[13],
        "data": res[14],
    }

    return result


def backout_order(id, number):
    try:
        ins = orders.update().values(status="backout").where(orders.c.id == id).where(orders.c.user == number)
        fin = conn.execute(ins)
        return {"server_status": 200}
    except:
        return {"server_status": 401}


engine = create_engine(db_connect, echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()

import json
import datetime

from decouple import config
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, insert, update, Boolean, \
    DateTime
from sqlalchemy.dialects.postgresql import JSONB

from users.orderAndProduct.products import Product

# db_connect = config('database-connect-addres')
# meta = MetaData()
product = Product()

class CartDB:
    db_connect = config('database-connect-addres')
    engine = create_engine(db_connect, echo=False, pool_size=6)

    # time_now = datetime.datetime.now() + tz_moscow

    def __init__(self):
        self.conn = self.engine.connect()
        meta = MetaData()
        self.cart = Table('cart1', meta,
                          Column('id', Integer(), primary_key=True),
                          Column('user', String(), default=None),
                          Column('pizzas', JSONB(), default=None),
                          Column('drinks', JSONB(), default=None),
                          Column('dessert', JSONB(), default=None),
                          Column('promocode', String(), default=None),
                          Column('promocode_item', String(), default=None),
                          Column('device', String(), default=None),
                          Column('price', Integer(), default=None),
                          Column('datetime', DateTime(), default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                          )
        meta.create_all(self.engine)

    # def new_db(self):
    #     meta = MetaData()
    #     self.cart = Table('cart', meta,
    #                   Column('id', Integer(), primary_key=True),
    #                   Column('user', String(), default=None),
    #                   Column('pizzas', JSON(), default=None),
    #                   Column('drinks', JSON(), default=None),
    #                   Column('dessert', JSON(), default=None),
    #                   Column('promocode', String(), default=None),
    #                   Column('promocode_item', String(), default=None),
    #                   Column('device', String(), default=None),
    #                   Column('price', Integer(), default=None),
    #                   Column('datetime', DateTime(), default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    #                   )
    #     meta.create_all(self.engine)

    def add_pizza(self, order_id, item_id):
        pizza = product.get_pizza(item_id)

        if order_id is None:
            ins = self.cart.insert().values(pizzas=pizza).returning(
                self.cart.c.id,
                self.cart.c.pizzas,
            )
            fin = self.conn.execute(ins).fetchone()
            return fin
        else:
            sel = select(self.cart.c.pizzas).where(self.cart.c.id == order_id)
            res = self.conn.execute(sel).fetchone()
            jsonres = []

            for i in res[0]:
                jsonres.append(
                    {
                    "id": i['id'],
                    "title": i['title'],
                    "description": i['description'],
                    "photo": i['photo'],
                    "price_small": i['price_small'],
                    "price_middle": i['price_middle'],
                    "price_big": i['price_big'],
                     }
                )
            jsonres.append(pizza)
            print(jsonres)
            upd = self.cart.update().values(pizzas=jsonres).where(self.cart.c.id == order_id).returning(
                self.cart.c.id,
                self.cart.c.pizzas,
            )
            resupd = self.conn.execute(upd).fetchone()
            # fin = {order_id: resupd}
            return resupd

# def backout_order(id):
#     ins = orders.update().values(status="backout").where(orders.c.id == id)
#     fin = conn.execute(ins)
#     # Доделать проверку на номер пользователя, который хочет удалить заказ

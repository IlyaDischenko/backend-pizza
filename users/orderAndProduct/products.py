from sqlalchemy import create_engine, select, Table, Column, Integer, String, Boolean, MetaData, insert, update
from decouple import config

db_connect = config('database-connect-addres')

meta = MetaData()

pizzas = Table('pizzas', meta,
               Column('id', Integer(), primary_key=True),
               Column('title', String(255)),
               Column('description', String()),
               Column('category', Integer()),
               Column('photo', String()),
               Column('price_small', Integer()),
               Column('price_middle', Integer()),
               Column('price_big', Integer()),
               Column('is_view', Boolean(), default=True),
               )

drinks = Table('drinks', meta,
               Column('id', Integer(), primary_key=True),
               Column('title', String(255)),
               Column('description', String(), default=None),
               Column('photo', String()),
               Column('price', Integer()),
               Column('is_view', Boolean(), default=True),
               )


class Product:
    db_connect = config('database-connect-addres')
    engine = create_engine(db_connect, echo=False, pool_size=6)

    def __init__(self):
        self.conn = self.engine.connect()
        meta = MetaData()
        self.pizzas = Table('pizzas', meta,
                            Column('id', Integer(), primary_key=True),
                            Column('title', String(255)),
                            Column('description', String()),
                            Column('category', Integer()),
                            Column('photo', String()),
                            Column('price_small', Integer()),
                            Column('price_middle', Integer()),
                            Column('price_big', Integer()),
                            Column('is_view', Boolean(), default=True),
                            )

    def get_pizza(self, id):
        sel = select(
            [pizzas.c.id, pizzas.c.title, pizzas.c.description, pizzas.c.photo, pizzas.c.price_small,
             pizzas.c.price_middle, pizzas.c.price_big]).where(pizzas.c.id == id).where(pizzas.c.is_view == True)
        res = conn.execute(sel).fetchone()

        ret = {
            "id": res[0],
            "title": res[1],
            "description": res[2],
            "photo": res[3],
            "price_small": res[4],
            "price_middle": res[5],
            "price_big": res[6],
        }
        return ret


def get_pizzas():
    # Берём пиццы из базы и возвращаем пользователю
    sel = select(
        [pizzas.c.id, pizzas.c.title, pizzas.c.description, pizzas.c.category, pizzas.c.photo, pizzas.c.price_small,
         pizzas.c.price_middle, pizzas.c.price_big]).where(pizzas.c.is_view == True)
    res = conn.execute(sel).fetchall()
    return res


def get_drinks():
    # Берём напитки из базы и возвращаем пользователю
    sel = select(
        [drinks.c.id, drinks.c.title, drinks.c.description, drinks.c.photo, drinks.c.price]).where(
        drinks.c.is_view == True)
    res = conn.execute(sel).fetchall()
    return res


def check_pizzas(pizza):
    result = []
    local_sum = 0
    sum = 0
    if len(pizza) > 0:
        for i in pizza:
            if i["size"] == 25:
                sel = select([pizzas.c.is_view, pizzas.c.price_small]).where(pizzas.c.id == i["id"])
                res = conn.execute(sel).fetchone()

                if res[0]:
                    continue
                elif not res[0]:
                    return False
            elif i["size"] == 30:
                sel = select([pizzas.c.is_view, pizzas.c.price_middle]).where(pizzas.c.id == i["id"])
                res = conn.execute(sel).fetchone()

                if res[0]:
                    continue
                elif not res[0]:
                    return False
            elif i["size"] == 35:
                sel = select([pizzas.c.is_view, pizzas.c.price_big]).where(pizzas.c.id == i["id"])
                res = conn.execute(sel).fetchone()

                if res[0]:
                    continue
                elif not res[0]:
                    return False
        return True
    else:
        return True


def get_pizza_sum(pizza):
    sum = 0
    for i in pizza:
        if i["size"] == 25:
            sel = select([pizzas.c.is_view, pizzas.c.price_small]).where(pizzas.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            sum = sum + (res[1] * i["count"])


        elif i["size"] == 30:
            sel = select([pizzas.c.is_view, pizzas.c.price_middle]).where(pizzas.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            sum = sum + (res[1] * i["count"])

        elif i["size"] == 35:
            sel = select([pizzas.c.is_view, pizzas.c.price_big]).where(pizzas.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            sum = sum + (res[1] * i["count"])

    return sum


def check_drinks(drink):
    if len(drink) != 0:
        for i in drink:
            sel = select([drinks.c.is_view, drinks.c.price]).where(drinks.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            if res[0]:
                continue
            elif not res[0]:
                return False
        return True
    else:
        return True


def get_drink_sum(drink):
    sum = 0
    for i in drink:
        sel = select([drinks.c.is_view, drinks.c.price]).where(drinks.c.id == i["id"])
        res = conn.execute(sel).fetchone()

        sum = sum + (res[1] * i["count"])

    return sum


engine = create_engine(db_connect, echo=False, pool_size=8)
meta.create_all(engine)
conn = engine.connect()

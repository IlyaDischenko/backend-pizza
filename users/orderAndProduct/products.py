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
    for i in pizza:
        if i["size"] == 25:
            sel = select([pizzas.c.is_view, pizzas.c.price_small]).where(pizzas.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            if res[0]:
                local_sum = res[1]
                sum = sum + (local_sum * i["count"])
                continue
            elif not res[0]:
                return False
        elif i["size"] == 30:
            sel = select([pizzas.c.is_view, pizzas.c.price_middle]).where(pizzas.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            if res[0]:
                local_sum = res[1]
                sum = sum + (local_sum * i["count"])
                continue
            elif not res[0]:
                return False
        elif i["size"] == 35:
            sel = select([pizzas.c.is_view, pizzas.c.price_big]).where(pizzas.c.id == i["id"])
            res = conn.execute(sel).fetchone()

            if res[0]:
                local_sum = res[1]
                sum = sum + (local_sum * i["count"])
                continue
            elif not res[0]:
                return False
    return sum

def check_drinks(drink):
    local_sum = 0
    sum = 0
    for i in drink:
        sel = select([drinks.c.is_view, drinks.c.price]).where(drinks.c.id == i["id"])
        res = conn.execute(sel).fetchone()

        if res[0]:
            local_sum = res[1]
            sum = sum + (local_sum * i["count"])
            continue
        elif not res[0]:
            return False

    return sum



engine = create_engine(db_connect, echo=False, pool_size=8)
meta.create_all(engine)
conn = engine.connect()

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
               Column('description', String(), default="None"),
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


engine = create_engine(db_connect, echo=False, pool_size=8)
meta.create_all(engine)
conn = engine.connect()

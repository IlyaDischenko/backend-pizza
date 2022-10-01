from sqlalchemy import create_engine, select, Table, Column, Integer, String, Boolean, MetaData, insert, update

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
               Column('description', String()),
               Column('photo', String()),
               Column('price', Integer()),
               Column('is_view', Boolean(), default=True),
               )


def get_pizzas():
    # Берём пиццы из базы и возвращаем пользователю
    sel = select([pizzas.c.id, pizzas.c.title, pizzas.c.description, pizzas.c.category, pizzas.c.photo, pizzas.c.price_small, pizzas.c.price_middle, pizzas.c.price_big]).where(pizzas.c.is_view == True)
    res = conn.execute(sel).fetchall()
    return res


def get_drinks():
    # Берём напитки из базы и возвращаем пользователю
    sel = select(
        [drinks.c.id, drinks.c.title, drinks.c.description, drinks.c.photo, drinks.c.price]).where(drinks.c.is_view == True)
    res = conn.execute(sel).fetchall()
    return res

engine = create_engine(
    "postgresql://yeikikepummkph:efe3f9c86b97c3fc4d42b6698b594d83df58ac07579548e12e3cd543557c86d2@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/dbk7asg84aedin",
    echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()
from sqlalchemy import create_engine, select, Table, Column, Integer, String, Boolean, MetaData, insert, update

meta = MetaData()

pizzas = Table('pizzas', meta,
               Column('id', Integer(), primary_key=True),
               Column('title', String(255)),
               Column('description', String(255)),
               Column('photo', String(255)),
               Column('price_small', Integer()),
               Column('price_middle', Integer()),
               Column('price_big', Integer()),
               Column('is_view', Boolean(), default=True),
               )


def get_pizzas():
    # Проверка кода введённого пользователем
    sel = select([pizzas.c.id, pizzas.c.title, pizzas.c.description, pizzas.c.photo, pizzas.c.price_small, pizzas.c.price_middle, pizzas.c.price_big]).where(pizzas.c.is_view == True)
    res = conn.execute(sel).fetchall()
    print(res)
    return res


engine = create_engine(
    "postgresql://yeikikepummkph:efe3f9c86b97c3fc4d42b6698b594d83df58ac07579548e12e3cd543557c86d2@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/dbk7asg84aedin",
    echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()
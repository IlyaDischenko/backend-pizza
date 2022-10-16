
from decouple import config
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, insert, update, Boolean

db_connect = config('database-connect-addres')
meta = MetaData()

discount_percent = Table('discount_percent', meta,
              Column('id', Integer(), primary_key=True),
              Column('promocode', String(255), unique=True),
              Column('count', Integer()),
              Column('percent', Integer()),
              Column('is_view', Boolean(), default=True),
              )

discount_rub = Table('discount_rub', meta,
              Column('id', Integer(), primary_key=True),
              Column('promocode', String(255), unique=True),
              Column('count', Integer()),
              Column('rub', Integer()),
              Column('is_view', Boolean(), default=True),
              )

promo_items = Table('promo_items', meta,
                Column('id', Integer(), primary_key=True),
                Column('promocode', String(255), unique=True),
                Column('title', String(255)),
                Column('description', String(), default="None"),
                Column('photo', String()),
                Column('price', Integer()),
                Column('count', Integer()),
                Column('is_view', Boolean(), default=True),
              )



def check_percent(promo):
    sel = select([discount_percent.c.percent, discount_percent.c.count, discount_percent.c.is_view]).where(discount_percent.c.promocode == promo)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        return False
    elif len(res) != 0:
        if res[0][2] == True and res[0][1] != 0:
            # -1 К ИСПОЛЬЗОВАНИЮ СДЕЛАТЬ НЕ ЗАБЫТЬ НА ФУНКЦИЮ ИСПОЛЬЗОВАНИЯ ПРОМОКОДА
            # ins = discount_percent.update().values(count = res[0][1] - 1).where(discount_percent.c.promocode == promo)
            # fin = conn.execute(ins)
            return res[0][0]
        else:
            return False

def check_rub(promo):
    sel = select([discount_rub.c.rub, discount_rub.c.count, discount_rub.c.is_view]).where(discount_rub.c.promocode == promo)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        return False
    elif len(res) != 0:
        if res[0][2] == True and res[0][1] != 0:
            # -1 К ИСПОЛЬЗОВАНИЮ СДЕЛАТЬ НЕ ЗАБЫТЬ НА ФУНКЦИЮ ИСПОЛЬЗОВАНИЯ ПРОМОКОДА
            # ins = discount_percent.update().values(count = res[0][1] - 1).where(discount_percent.c.promocode == promo)
            # fin = conn.execute(ins)
            return res[0][0]
        else:
            return False

def check_items(promo):
    sel = select([promo_items.c.title, promo_items.c.description, promo_items.c.photo, promo_items.c.price,
                  promo_items.c.count, promo_items.c.is_view]).where(promo_items.c.promocode == promo)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        return False
    elif len(res) != 0:
        if res[0][5] == True and res[0][4] != 0:
            # -1 К ИСПОЛЬЗОВАНИЮ СДЕЛАТЬ НЕ ЗАБЫТЬ НА ФУНКЦИЮ ИСПОЛЬЗОВАНИЯ ПРОМОКОДА
            # ins = discount_percent.update().values(count = res[0][1] - 1).where(discount_percent.c.promocode == promo)
            # fin = conn.execute(ins)
            return {
                "title": res[0][0],
                "description": res[0][1],
                "photo": res[0][2],
                "price": res[0][3],
            }

        else:
            return False



engine = create_engine(db_connect, echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()
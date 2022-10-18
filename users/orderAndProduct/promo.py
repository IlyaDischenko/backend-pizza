from decouple import config
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, insert, update, Boolean

db_connect = config('database-connect-addres')
meta = MetaData()

discount = Table('discount1', meta,
                 Column('id', Integer(), primary_key=True),
                 Column('promocode', String(255), unique=True),
                 Column('count', Integer()),
                 Column('type', String(255)),

                 Column('return_data', String()),

                 Column('min_sum', Integer()),
                 Column('need_number', Boolean()),
                 Column('number', String(255)),
                 Column('is_view', Boolean(), default=True),
                 )


def check_discount(promo, number):
    sel = select([discount.c.id, discount.c.count, discount.c.type, discount.c.return_data, discount.c.min_sum,
                  discount.c.need_number, discount.c.number, discount.c.is_view]).where(discount.c.promocode == promo)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        return {"status": 400}
    elif len(res) != 0:
        if res[0][7] and res[0][1] != 0:
            if not res[0][5]:
                return {"type": res[0][2], "min_sum": res[0][4], "discount_data": res[0][3], "status": 200}
            elif res[0][5] and res[0][6] != number:
                return {"status": 401}
            elif res[0][5] and res[0][6] == number:
                return {"type": res[0][2], "min_sum": res[0][4], "discount_data": res[0][3], "status": 200}

        else:
            return {"status": 422}


engine = create_engine(db_connect, echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()

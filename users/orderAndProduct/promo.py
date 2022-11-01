import json
import datetime

from decouple import config
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, insert, update, Boolean, DateTime

db_connect = config('database-connect-addres')
meta = MetaData()

discount = Table('discount', meta,
                 Column('id', Integer(), primary_key=True),
                 Column('promocode', String(255), unique=True),
                 Column('count', Integer()),
                 Column('type', Integer()),

                 Column('return_data', String()),

                 Column('min_sum', Integer()),
                 Column('need_number', Boolean()),
                 Column('number', String(255)),
                 Column('is_view', Boolean(), default=True),
                 )




def insert_json(promocode, count, type, return_data, min_sum, need_number, number, is_view):
    ins = discount.insert().values(promocode=promocode, count=count, type=type, return_data=return_data,
                                   min_sum=min_sum, need_number=need_number, number=number, is_view=is_view)
    fin = conn.execute(ins)


def check_discount(promo, number):
    sel = select([discount.c.id, discount.c.count, discount.c.type, discount.c.return_data, discount.c.min_sum,
                  discount.c.need_number, discount.c.number, discount.c.is_view]).where(discount.c.promocode == promo)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        return {"status": 400}
    elif len(res) != 0:
        if res[0][7] and res[0][1] != 0:
            # Проверка на количество промокодов
            if not res[0][5]:
                # Нужен ли номер, или промокод для всех
                if res[0][2] == 3:
                    # Проверка на json
                    return {"type": res[0][2], "min_sum": res[0][4], "discount_data": json.loads(res[0][3]), "status": 200}
                else:
                    return {"type": res[0][2], "min_sum": res[0][4], "discount_data": res[0][3], "status": 200}
            elif res[0][5] and res[0][6] != number:
                # Если нужен, то проверка номера
                return {"status": 401}
            elif res[0][5] and res[0][6] == number:
                # Если нужен, то проверка номера
                if res[0][2] == 3:
                    # Проверка на json
                    return {"type": res[0][2], "min_sum": res[0][4], "discount_data": json.loads(res[0][3]),
                            "status": 200}
                else:
                    return {"type": res[0][2], "min_sum": res[0][4], "discount_data": res[0][3], "status": 200}

        else:
            return {"status": 422}


engine = create_engine(db_connect, echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()

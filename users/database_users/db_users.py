import time
from decouple import config
db_connect = config('database-connect-addres')

from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, insert, update

meta = MetaData()

users = Table('Users', meta,
              Column('id', Integer(), primary_key=True),
              Column('name', String(50)),
              Column('email', String(100), unique=True),
              Column('number', String(50), unique=True),

              Column('city', String(100), default='Орёл'),
              Column('street', String(100)),
              Column('house', String(100)),
              Column('entrance', String(50)),
              Column('floor', String(50)),
              Column('apartment', String(50))
              )


last_active = Table('last_active', meta,
                    Column('id', Integer(), primary_key=True),
                    Column('id_user', Integer()),
                    Column('last_login', String(255))
                    )

valid_code = Table('valid_code', meta,
                   Column('id', Integer(), primary_key=True),
                   Column('number', String(255)),
                   Column('code', String(255)),
                   Column('data', String(255))
                   )


def insert_code(number, code):
    # Получаем от сервиса валидный код и добавляем в базу
    sel = select([valid_code.c.number]).where(valid_code.c.number == number)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        # Если такого номера ещё нет, то добавляем его, код, и дату добавления кода
        d = time.time() + 1200
        ins = valid_code.insert().values(number=number, code=code, data=d)
        fin = conn.execute(ins)
        return True
    elif len(res) != 0:
        # Если такой номер есть, то обновляем код и дату обновления кода
        d = time.time() + 1200
        ins = valid_code.update().values(code=code, data=d).where(valid_code.c.number == number)
        fin = conn.execute(ins)
        return True


def check_code(number, code):
    # Проверка кода введённого пользователем
    sel = select([valid_code.c.number, valid_code.c.code, valid_code.c.data]).where(valid_code.c.number == number)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        # Если кода нет, то возвращаем False
        return False
    elif len(res) != 0:
        # Если код есть, то проверяем дату и сравниваем его с введённым
        if float(res[0][2]) >= time.time():
            # Проверка на дату кода
            if res[0][1] == code:
                # Если код правильный, то возвращаем True
                return True
            elif res[0][1] != code:
                # Если код неправильный, то возвращаем True
                return False
        else:
            return False


def exists_user_or_add(number):
    # Проверка наличия пользователя в базе данных
    sel = select([users.c.number, users.c.id]).where(users.c.number == number)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        # Если пользователя нет, то создаем его и достаем его ID
        ins = users.insert().values(name=None, email=None, number=number)
        fin = conn.execute(ins)
        sel = select([users.c.id]).where(users.c.number == number)
        res = conn.execute(sel).fetchall()
        return res[0][0]

    elif len(res) != 0:
        # Если пользователь есть, то достаем его ID
        id = res[0][1]
        return id


def update_last_active(id):
    # Обновляем дату последней активности
    sel = select([last_active.c.id_user]).where(last_active.c.id_user == id)
    res = conn.execute(sel).fetchall()

    if len(res) < 1:
        # Если записей о пользователе нет, то создаем
        ins = last_active.insert().values(id_user=id, last_login=time.time())
        fin = conn.execute(ins)
        return True

    elif len(res) != 0:
        # Если пользователь есть, то обновляем дату
        ins = last_active.update().values(last_login=time.time()).where(last_active.c.id_user == id)
        fin = conn.execute(ins)
        return True


def add_email(id, email):
    # Добавляем почту
    try:
        ins = users.update().values(email=email).where(users.c.id == id)
        fin = conn.execute(ins)
        return True
    except:
        return False


def add_name(id, name):
    # Добавляем имя
    try:
        ins = users.update().values(name=name).where(users.c.id == id)
        fin = conn.execute(ins)
        return True
    except:
        return False


def add_address(id, street, house, entrance, floor, apartment):
    try:
        ins = users.update().values(street=street, house=house, entrance=entrance, floor=floor,
                                    apartment=apartment).where(users.c.id == id)
        fin = conn.execute(ins)
        return True
    except:
        return False


def get_profile_info(id):
    # Берём пиццы из базы и возвращаем пользователю
    sel = select(
        [users.c.name, users.c.email, users.c.number, users.c.street, users.c.house, users.c.entrance, users.c.floor, users.c.apartment]).where(users.c.id == id)
    res = conn.execute(sel).fetchall()
    return res


engine = create_engine(db_connect, echo=False, pool_size=6)
meta.create_all(engine)
conn = engine.connect()

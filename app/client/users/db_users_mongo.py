import time
import pymongo
from bson.objectid import ObjectId
from decouple import config

mongo_addres = config('mongo-db-addres')

db_client = pymongo.MongoClient(mongo_addres)
db = db_client['pizza_db']
street_collection = db['streets']
valid_code_collection = db['valid_code']
users_collection = db['users']


def get_streets():
    res_streets = street_collection.find({"is_view": True})
    ret_streets = []
    for i in res_streets:
        ret_streets.append(i["street"])
    return ret_streets


def insert_code(number, code):
    # Получаем от сервиса валидный код и добавляем в базу
    if valid_code_collection.find_one({"number": number}) is None:
        # Если такого номера ещё нет, то добавляем его, код, и дату добавления кода
        d = time.time() + 1200
        valid_code_collection.insert_one({"number": number, "code": code, "data": d})
        return True
    else:
        # Если есть такой номер, то обновляем
        d = time.time() + 1200
        valid_code_collection.update_one({"number": number}, {"$set": {"code": code, "data": d}})
        return True


def check_code(number, code):
    # Проверка кода введённого пользователем
    res = valid_code_collection.find_one({"number": number})

    if res is None:
        # Если кода нет, то возвращаем False
        return False
    elif res != None:
        # Если код есть, то проверяем дату и сравниваем его с введённым
        if float(res["data"]) >= time.time():
            # Проверка на дату кода
            if res["code"] == code:
                # Если код правильный, то возвращаем True
                return True
            else:
                # Если код неправильный, то возвращаем False
                return False
        else:
            return False


def exists_user_or_add(number):
    # Проверка наличия пользователя в базе данных

    res = users_collection.find_one({"number": number})

    if res is None:
        # Если пользователя нет, то создаем его и достаем его ID

        i = users_collection.insert_one({"number": number, "name": None, "email": None}).inserted_id

        return str(i)

    elif res != None:
        # Если пользователь есть, то достаем его ID

        ret = users_collection.find_one({"number": number})

        return str(ret["_id"])


# def update_last_active(id):
#     # ПЕРЕПИСАТЬ НА МОНГО!!!
#
#     # Обновляем дату последней активности
#     sel = select([last_active.c.id_user]).where(last_active.c.id_user == id)
#     res = conn.execute(sel).fetchall()
#
#     if len(res) < 1:
#         # Если записей о пользователе нет, то создаем
#         ins = last_active.insert().values(id_user=id, last_login=time.time())
#         fin = conn.execute(ins)
#         return True
#
#     elif len(res) != 0:
#         # Если пользователь есть, то обновляем дату
#         ins = last_active.update().values(last_login=time.time()).where(last_active.c.id_user == id)
#         fin = conn.execute(ins)
#         return True


def add_email(id, email):
    # Добавляем почту
    try:
        users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"email": email}})
        return True
    except:
        return False


def add_name(id, name):
    # Добавляем имя
    try:
        users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": name}})
        return True
    except:
        return False


# def add_address(id, street, house, entrance, floor, apartment):
#     try:
#         ins = users.update().values(street=street, house=house, entrance=entrance, floor=floor,
#                                     apartment=apartment).where(users.c.id == id)
#         fin = conn.execute(ins)
#         return True
#     except:
#         return False


def get_profile_info(id):
    # Возвращаем информацию пользователя
    ret = users_collection.find_one({"_id": ObjectId(id)})

    return {
        "number": ret["number"],
        "name": ret["name"],
        "email": ret["email"],
    }


def get_user_number(id):
    # Возвращаем номер пользователя
    ret = users_collection.find_one({"_id": ObjectId(id)})
    return ret["number"]

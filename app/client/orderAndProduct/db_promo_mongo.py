import time
import pymongo
from bson.objectid import ObjectId
from decouple import config


mongo_addres = config('mongo-db-addres')

db_client = pymongo.MongoClient(mongo_addres)
db = db_client['pizza_db']
promocode_collection = db['promocode']


def insert_promocode(promocode, count, type, discount_data, min_sum, need_number, number, is_view):
    promocode_collection.insert_one({
        "promocode": str(promocode),
        "count": int(count),
        "type": int(type),
        "discount_data": int(discount_data),
        "min_sum": int(min_sum),
        "need_number": bool(need_number),
        "number": str(number),
        "is_view": bool(is_view),
    })

def check_discount(promo, number):
    res = promocode_collection.find_one({"promocode": promo})

    if res is None:
        return {"status": 400}
    elif res != None:
        if res["is_view"] and res["count"] != 0:
            # Проверка на количество промокодов
            if not res["need_number"]:
                # Нужен ли номер, или промокод для всех
                # if res["type"] == 3:

                # Проверка на json
                return {"type": res["type"], "min_sum": res["min_sum"], "discount_data": res["discount_data"], "status": 200}

                # else:
                #     return {"type": res[0][2], "min_sum": res[0][4], "discount_data": res[0][3], "status": 200}
            elif res["need_number"] and res["number"] != number:
                # Если нужен, то проверка номера
                return {"status": 401}
            elif res["need_number"] and res["number"] == number:
                # Если нужен, то проверка номера
                # if res[0][2] == 3:

                # Проверка на json
                return {"type": res["type"], "min_sum": res["min_sum"], "discount_data": res["discount_data"],
                            "status": 200}
                # else:
                #     return {"type": res[0][2], "min_sum": res[0][4], "discount_data": res[0][3], "status": 200}

        else:
            return {"status": 422}
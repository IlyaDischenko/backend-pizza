import time
import pymongo
from bson.objectid import ObjectId
from decouple import config

from client.order.db_order_mongo import check_order_by_id

mongo_addres = config('mongo-db-addres')

db_client = pymongo.MongoClient(mongo_addres)
db = db_client['pizza_db']
promocode_collection = db['promocode']
order_collection = db['orders']


def insert_promocode(promocode, count, type, discount_data, min_sum, max_sum, need_number, number, is_view):
    promocode_collection.insert_one({
        "promocode": str(promocode),
        "count": int(count),
        "type": int(type),
        "discount_data": int(discount_data),
        "min_sum": int(min_sum),
        "max_sum": int(max_sum),
        "need_number": bool(need_number),
        "number": str(number),
        "is_view": bool(is_view),
    })


def add_promocode(promocode, id=None):
    obj = check_order_by_id(id)
    promo_data = promocode_collection.find_one({"promocode": promocode, "is_view": True})

    if promo_data is None or promo_data["count"] <= 0:
        # Если промокода нет или он закончился
        obj["promo"]["promocode"] = ""
        obj["promo"]["promocode_type"] = ""
        obj["promo"]["promocode_take"] = False
        obj["promo"]["promocode_applied"] = False
        obj["promo"]["promocode_message"] = "Такой промокод не найден"
        obj["promo"]["promocode_effect"] = ""
        obj["promo"]["promocode_min_sum"] = ""
        obj["promo"]["promocode_max_sum"] = ""

        obj["total_sum_with_promo"] = obj["total_sum_without_promo"]
    else:
        # Если промокод есть

        if not promo_data["need_number"] or obj["number"] == promo_data["number"]:
            # Если не нужен номер, или номер совпадает (тоесть человек авторизован)

            # Отдельно пишу переменные, которые не нужно считать
            obj["promo"]["promocode"] = promo_data["promocode"]
            obj["promo"]["promocode_type"] = promo_data["type"]
            obj["promo"]["promocode_take"] = True

            obj["promo"]["promocode_effect"] = promo_data["discount_data"]
            obj["promo"]["promocode_min_sum"] = promo_data["min_sum"]
            obj["promo"]["promocode_max_sum"] = promo_data["max_sum"]
            if obj["count_items"] <= 0:
                # Если в корзине не было элементов до этого
                obj["promo"]["promocode_applied"] = False
                obj["promo"]["promocode_message"] = "Промокод применён, добавьте товар"

                obj["total_sum_with_promo"] = obj["total_sum_without_promo"]
            else:
                # Если в корзине были элементы
                c_sum = int(obj["total_sum_without_promo"])
                c_min_sum = int(promo_data["min_sum"])
                c_max_sum = int(promo_data["max_sum"])

                if c_sum >= c_min_sum and c_sum <= c_max_sum:
                    # Если сумма заказа в допустимой норме минимальной и максимальной суммы промокода
                    obj["promo"]["promocode_applied"] = True
                    obj["promo"]["promocode_message"] = "Промокод применён"


                    if promo_data["type"] == "percent":
                        # Если промокод вычитает проценты
                        obj["total_sum_with_promo"] = int((float(obj["total_sum_without_promo"]) / 100) * (100 - int(promo_data["discount_data"])))
                    elif promo_data["type"] == "sum":
                        # Если промокод отнимает сумму
                        obj["total_sum_with_promo"] = int(obj["total_sum_without_promo"]) - int(promo_data["discount_data"])

                else:
                    # Если минимальная или максимальная сумма заказа не подходит
                    obj["promo"]["promocode_applied"] = False
                    obj["promo"]["promocode_message"] = f"Минимальная сумма заказа {c_min_sum}"

                    obj["total_sum_with_promo"] = obj["total_sum_without_promo"]

        elif promo_data["need_number"] and obj["number"] != promo_data["number"]:
            # Если нужен телефон, а пользователь не авторизован
            obj["promo"]["promocode"] = ""
            obj["promo"]["promocode_type"] = ""
            obj["promo"]["promocode_take"] = False
            obj["promo"]["promocode_applied"] = False
            obj["promo"]["promocode_message"] = "Авторизуйтесь по номеру телефона на который был выдан промокод"
            obj["promo"]["promocode_effect"] = ""
            obj["promo"]["promocode_min_sum"] = ""
            obj["promo"]["promocode_max_sum"] = ""

            obj["total_sum_with_promo"] = obj["total_sum_without_promo"]

    order_collection.update_one({"_id": ObjectId(str(obj["_id"]))}, {"$set": {"order_id": str(obj["_id"]),
                                                                              "promo": obj["promo"],
                                                                              "total_sum_with_promo": obj[
                                                                                  "total_sum_with_promo"],
                                                                              }})

    return order_collection.find_one({"_id": ObjectId(str(obj["_id"]))}, {'_id': False})



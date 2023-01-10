import datetime
from bson.objectid import ObjectId
import pymongo
from decouple import config

# from client.orderAndProduct.db_promo_mongo import get_promocode

mongo_addres = config('mongo-db-addres')

db_client = pymongo.MongoClient(mongo_addres)
db = db_client['pizza_db']
pizza_collection = db['pizza']
drink_collection = db['drink']
app_config_collection = db['app_config']

order_collection = db['orders']


def check_order_by_id(id):
    # Функция либо вернёт объект заказа, либо создаст его и вернёт

    if len(id) == 0 or len(id) < 24:
        check = None
    else:
        check = order_collection.find_one({"_id": ObjectId(id)})

    if check is None:
        return set_null_order()
    else:
        return check


def set_null_order():
    # Функция создаст пустой ордер

    null_order = {
        "order_id": "",
        "number": "",
        "pizza": {
            "items": [],
            "count_pizza": 0,
            "total_pizza": 0
        },
        "drink": {
            "items": [],
            "count_drink": 0,
            "total_drink": 0
        },
        "dessert": {
            "items": [],
            "count_dessert": 0,
            "total_dessert": 0
        },
        "token": "",
        "is_login": False,
        "can_order": False,
        "cant_order_message": "",
        "points": {
            "points_for_order": 0,
            "item_for_points": {},
            "item_for_points_price": 0,
            "use_item_for_points": False
        },
        "total_sum_without_promo": 0,
        "total_sum_with_promo": 0,
        "count_items": 0,
        "datetime": datetime.datetime.now(),
        "promo": {
            "promocode": "",
            "promocode_take": False,
            "promocode_applied": False,
            "promocode_message": "",
            "promocode_type": "",
            "promocode_effect": "",
            "promocode_min_sum": "",
            "promocode_max_sum": ""
        },
        "addres": {
            "city": "",
            "street": "",
            "house": "",
            "entrance": "",
            "floor": "",
            "apartment": ""
        },
        "comment": "",
        "device": "",
        "paytype": "",
        "status": "initial"
    }
    return order_collection.find_one({"_id": ObjectId(str(order_collection.insert_one(null_order).inserted_id))})


def add_pizza(item_id, id=None):
    obj = check_order_by_id(id)
    # Получаю пиццу из бд
    pizza = pizza_collection.find_one({"_id": ObjectId(item_id[:-2]), "is_view": True})

    exists = False
    pizza_item_price = None
    # item_points =

    # Если такой пиццы нет в базе, то возвращаем исходный объект
    if pizza is None:
        return obj

    # Записываю в переменную цену за пиццу согласно размеру
    if item_id[-2:] == "26":
        pizza_item_price = int(pizza["price_small"])
    if item_id[-2:] == "30":
        pizza_item_price = int(pizza["price_middle"])
    if item_id[-2:] == "35":
        pizza_item_price = int(pizza["price_big"])

    # Ищу пиццу в уже записанных и если нахожу, то добавляю в количество и пересчитываю цену
    for i in obj["pizza"]["items"]:
        if i["id"] == item_id:
            i["count"] = str(int(i["count"]) + 1)
            i["price"] = str(int(i["price"]) + pizza_item_price)

            obj["pizza"]["count_pizza"] = str(int(obj["pizza"]["count_pizza"]) + 1)
            obj["pizza"]["total_pizza"] = str(int(obj["pizza"]["total_pizza"]) + pizza_item_price)
            # obj["pizza"]["total_points"] = str(int(obj["pizza"]["total_points"]) + item_points)

            exists = True
            break

    # Если пиццы нет, то добавляю ее
    if not exists:
        obj["pizza"]["items"].append({
            "id": item_id,
            "title": pizza["title"],
            "size": item_id[-2:],
            "photo": pizza["photo"],
            "count": "1",
            "price": str(pizza_item_price),
        })
        obj["pizza"]["count_pizza"] = str(int(obj["pizza"]["count_pizza"]) + 1)
        obj["pizza"]["total_pizza"] = str(int(obj["pizza"]["total_pizza"]) + pizza_item_price)

    res_math = math(obj)


    order_collection.update_one({"_id": ObjectId(str(obj["_id"]))}, {"$set": {"order_id": str(obj["_id"]),
                                                                              "pizza": obj["pizza"],
                                                                              "promo": res_math["promo"],
                                                                              "total_sum_without_promo": res_math[
                                                                                  "total_sum_without_promo"],
                                                                              "total_sum_with_promo": res_math[
                                                                                  "total_sum_with_promo"],
                                                                              "count_items": res_math["count_items"]}})

    return order_collection.find_one({"_id": ObjectId(str(obj["_id"]))}, {'_id': False})


def math(obj):
    obj["total_sum_without_promo"] = int(obj["pizza"]["total_pizza"]) + int(obj["drink"]["total_drink"]) + int(
        obj["dessert"]["total_dessert"])
    obj["count_items"] = int(obj["pizza"]["count_pizza"]) + int(obj["drink"]["count_drink"]) + int(
        obj["dessert"]["count_dessert"])

    if not obj["promo"]["promocode_take"]:
        return {
            "promo": obj["promo"],
            "total_sum_without_promo": obj["total_sum_without_promo"],
            "total_sum_with_promo": obj["total_sum_without_promo"],
            "count_items": obj["count_items"]
        }
    else:

        if obj["count_items"] <= 0:
            # Если в корзине не было элементов до этого
            obj["promo"]["promocode_applied"] = False
            obj["promo"]["promocode_message"] = "Промокод применён, добавьте товар"

            obj["total_sum_with_promo"] = obj["total_sum_without_promo"]
        else:
            # Если в корзине были элементы
            c_sum = int(obj["total_sum_without_promo"])
            c_min_sum = int(obj["promo"]["promocode_min_sum"])
            c_max_sum = int(obj["promo"]["promocode_max_sum"])

            if c_min_sum <= c_sum <= c_max_sum:
                # Если сумма заказа в допустимой норме минимальной и максимальной суммы промокода
                obj["promo"]["promocode_applied"] = True
                obj["promo"]["promocode_message"] = "Промокод применён"

                if obj["promo"]["promocode_type"] == "percent":
                    # Если промокод вычитает проценты
                    obj["total_sum_with_promo"] = int(
                        (float(obj["total_sum_without_promo"]) / 100) * (100 - int(obj["promo"]["promocode_effect"])))
                elif obj["promo"]["promocode_type"] == "sum":
                    # Если промокод отнимает сумму
                    obj["total_sum_with_promo"] = int(obj["total_sum_without_promo"]) - int(
                        obj["promo"]["promocode_effect"])
            else:
                # Если минимальная или максимальная сумма заказа не подходит
                obj["promo"]["promocode_applied"] = False
                obj["promo"]["promocode_message"] = f"Минимальная сумма заказа {c_min_sum}"

                obj["total_sum_with_promo"] = obj["total_sum_without_promo"]

        return {
            "promo": obj["promo"],
            "total_sum_without_promo": obj["total_sum_without_promo"],
            "total_sum_with_promo": obj["total_sum_with_promo"],
            "count_items": obj["count_items"]
        }

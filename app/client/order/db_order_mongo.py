import datetime
from bson.objectid import ObjectId
import pymongo
from decouple import config

mongo_addres = config('mongo-db-addres')

db_client = pymongo.MongoClient(mongo_addres)
db = db_client['pizza_db']
pizza_collection = db['pizza']
drink_collection = db['drink']
app_config_collection = db['app_config']

order_collection = db['orders']


def check_order_by_id(id):
    # Функция либо вернёт объект заказа, либо создаст его и вернёт

    if len(id) == 0:
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
        "total_sum_without_promo": 0,
        "total_sum_with_promo": 0,
        "count_items": 0,
        "datetime": datetime.datetime.now(),
        "promo": {
            "promocode": "",
            "promocode_accepted": False,
            "promocode_message": "",
            "promocode_status": "",
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
        "status": ""
    }
    return order_collection.find_one({"_id": ObjectId(str(order_collection.insert_one(null_order).inserted_id))})


def add_pizza(item_id, id=None):
    obj = check_order_by_id(id)
    # Получаю пиццу из бд
    pizza = pizza_collection.find_one({"_id": ObjectId(item_id[:-2]), "is_view": True})

    exists = False
    pizza_item_price = None

    # Если такой пиццы нет в базе, то возвращаем исходный объект
    if pizza is None:
        return obj

    # Записываю в переменную цену за пиццу согласно размеру
    if item_id[-2:] == "27":
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

    order_collection.update_one({"_id": ObjectId(str(obj["_id"]))}, {"$set": {"pizza": obj["pizza"]}})

    xy = order_collection.find_one({"_id": ObjectId(str(obj["_id"]))}, {'_id': False})

    return xy

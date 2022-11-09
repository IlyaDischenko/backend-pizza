import datetime

import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from users.database_users.db_users import check_code, exists_user_or_add, add_email, add_name, add_address, \
    update_last_active, get_profile_info, get_user_number, get_streets
from users.database_users.model_users import Token, Number, Code, Email, Name, Address
from users.orderAndProduct.models_orderPromo import Promocode, Insert_promocode, Order
from users.orderAndProduct.products import get_pizzas, get_drinks, check_pizzas, check_drinks, get_drink_sum, \
    get_pizza_sum
from users.orderAndProduct.promo import check_discount, insert_json
from users.orderAndProduct.order import get_order, set_order
from users.singin.call import call_service
from users.singin.jwt_handler import getJWT, middleware, check_refresh

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://frontend-pizza-ehrg.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get/all")
def get_pizza():
    res_pizzas = get_pizzas()
    res_drinks = get_drinks()
    return {"pizza": res_pizzas,
            "drinks": res_drinks}


@app.post("/api/get/token")
def get_token(num: Number):
    # Функция для отправки номера в сервис и добавление валидного кода в базу
    call_service(num.number)
    return {"status": 200, "number": num.number}


@app.post("/api/confirmtoken")
def confirm_token(data: Code):
    # Функция для проверки кода о получения access токена
    res = check_code(number=data.number, code=data.code)
    if res:
        res = getJWT(exists_user_or_add(number=data.number))
        return {
            "status": 200,
            "token": res,
        }
    elif not res:
        return {"status": 400}


@app.post('/api/refreshtoken')
def refresh_token(data: Token):
    try:
        x = check_refresh(data.token)
        if x != False:
            res = getJWT(user_id=x)
            return {
                "access token": res,
                # "refresh token": res[1]
            }
        else:
            return {
                "status": 401,
                "error": "Not valid refresh token"
            }
    except:
        return {"status": 400}


@app.get("/api/get/userinfo")
def get_user_info(token: Token):
    check = middleware(token.token)
    if check != False:
        user_data = get_profile_info(check)
        return {"data": user_data}
    else:
        return {
            "status": 401,
            "error": "Not valid access token"
        }


@app.post("/api/get/userinfo")
def get_user_info_post(token: Token):
    check = middleware(token.token)
    if check != False:
        user_data = get_profile_info(check)
        return {
            "status": 200,
            "data": user_data}
    else:
        return {
            "status": 401,
            "error": "Not valid access token"
        }


@app.post("/api/set/email")
def set_email(data: Email):
    check = middleware(data.token)
    if check != False:
        add_result = add_email(id=check, email=data.email)
        update_last_active(check)
        if add_result == True:

            return {"status": 200}
        else:
            return {"status": 400}
    elif check == False:
        return {
            "status": 401,
            "error": "Not valid access token"
        }


@app.post("/api/set/name")
def set_name(data: Name):
    check = middleware(data.token)
    if check != False:
        res = add_name(id=check, name=data.name)
        update_last_active(check)
        if res == True:
            return {"status": 200}
        else:
            return {"status": 400}
    elif check == False:
        return {"status": 401}


@app.post("/api/set/address")
def set_address(data: Address):
    try:
        check = middleware(data.token)
        if check != False:
            add_address(id=check, street=data.street, house=data.house, entrance=data.entrance, floor=data.floor,
                        apartment=data.apartment)
            update_last_active(check)
            return {"status": 200}
        elif check == False:
            return {"status": 300}
    except:
        return {"status": 200}


@app.post("/api/check/promocode")
def check_promocode(data: Promocode):
    return check_discount(promo=data.promocode, number=data.number)


@app.post("/api/insert/promocode")
def insert_promocode(data: Insert_promocode):
    js = json.dumps(data.return_data)
    insert_json(promocode=data.promocode, count=data.count, type=data.type, return_data=js,
                min_sum=data.min_sum, need_number=data.need_number, number=data.number, is_view=data.is_view)
    return {"success": 1}


@app.post("/api/set/order")
def testPoint(data: Order):
    check = middleware(data.token)

    if check:
        # Не забыть поставить нормальное время при деплое
        tz_moscow = datetime.timedelta(hours=3)
        time_now = datetime.datetime.now() + tz_moscow

        if check_pizzas(data.pizzas) and check_drinks(data.drinks):
            sum = get_pizza_sum(data.pizzas) + get_drink_sum(data.drinks)

            dpizzas = json.dumps(data.pizzas)
            ddrinks = json.dumps(data.drinks)
            user_data = get_user_number(check)

            discount_data = None

            if len(data.promocode) > 0:
                z = check_discount(promo=data.promocode, number=user_data)
                if z['status'] == 200:
                    #  Если промокод успешно проверен
                    if z['type'] == 1:
                        #  Если тип промокода первый
                        if z['min_sum'] < sum:
                            #  Проверка на минимальную сумму
                            return {"status": 460}
                        else:
                            # Если всё нормально, то считаем сумму
                            sum = (sum // 100) * (100 - int(z['discount_data']))
                    elif z['type'] == 2:
                        #  Если тип промокода второй
                        if z['min_sum'] < sum:
                            #  Проверка на минимальную сумму
                            return {"status": 460}
                        else:
                            if sum - int(z['discount_data']) < 0:
                                # Если сумма со скидкой в рублях меньше нуля
                                return {"status": 461}
                            else:
                                sum -= int(z['discount_data'])
                    elif z['type'] == 3:
                        #  Если тип промокода третий
                        if z['min_sum'] < sum:
                            #  Проверка на минимальную сумму
                            return {"status": 460}
                        else:
                            discount_data = json.dumps(z['discount_data'])
                            sum += z['discount_data']['price']

                elif z['status'] == 400:
                    return {"status": 450}
                elif z['status'] == 401:
                    return {"status": 451}
                elif z['status'] == 422:
                    return {"status": 452}

            set_order(user=user_data, pizzas=dpizzas, drinks=ddrinks, promocode=data.promocode,
                      promocode_item=discount_data,
                      street=data.street, house=data.house, entrance=data.entrance,
                      floor=data.floor, apartment=data.apartment, device=data.device, paytype=data.paytype,
                      price=sum, comment=data.comment, status="accepted", data=time_now)
            return {"status": 200, "sum": sum}
        else:
            return {"status": 400}
    else:
        return {
            "status": 401,
            "error": "Not valid access token"
        }


@app.get("/api/get/order/accepted")
def testPoint():
    return get_order(status="accepted")


@app.get("/api/get/order/ready")
def testPoint():
    return get_order(status="ready")


@app.get("/api/get/street")
def getStreet():
    return {"status": 200, "street": get_streets()}

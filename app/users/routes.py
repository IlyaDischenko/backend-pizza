import datetime
import json

from fastapi import Request
from fastapi import APIRouter


from users.orderAndProduct.products import get_pizzas, get_drinks, check_pizzas, check_drinks, get_drink_sum, \
    get_pizza_sum
from users.database_users.db_users import check_code, exists_user_or_add, add_email, add_name, add_address, \
    update_last_active, get_profile_info, get_user_number, get_streets
from users.database_users.model_users import Token, Number, Code, Email, Name, Address
from users.orderAndProduct.models_orderPromo import Promocode, Insert_promocode, Order, GetOrder, BackoutOrder
from users.orderAndProduct.products import get_pizzas, get_drinks, check_pizzas, check_drinks, get_drink_sum, \
    get_pizza_sum
from users.orderAndProduct.promo import check_discount, insert_json, decrement_promo_count
from users.orderAndProduct.order import get_order, set_order, backout_order
from users.singin.call import call_service
from users.singin.jwt_handler import getJWT, middleware, check_refresh

router = APIRouter()

@router.get("/")
def null_req():
    return {"its": "ok"}


@router.get("/get/all")
def get_pizza():
    res_pizzas = get_pizzas()
    res_drinks = get_drinks()
    return {"pizza": res_pizzas,
            "drinks": res_drinks}

@router.post("/api/get/token")
def get_token(num: Number):
    # Функция для отправки номера в сервис и добавление валидного кода в базу
    call_service(num.number)
    return {"status": 200, "number": num.number}


@router.post("/api/confirmtoken")
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

# @router.post('/api/token/check')
# def check_access_token(data: Token):
#     check = middleware(data.token)

@router.post('/api/refreshtoken')
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


@router.post("/api/get/userinfo")
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


@router.post("/api/set/email")
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


@router.post("/api/set/name")
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

@router.post("/api/set/address")
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


@router.post("/api/check/promocode")
def check_promocode(data: Promocode):
    return check_discount(promo=data.promocode, number=data.number)


@router.post("/api/set/order")
def testPoint(data: Order):
    check = middleware(data.token)
    time_now = datetime.datetime.now()
    x = time_now.strftime('%H')
    if int(x) <= 10 or int(x) >= 24:
        return {"status": 462}

    if check:
        # Не забыть поставить нормальное время при деплое
        # tz_moscow = datetime.timedelta(hours=3)


        if check_pizzas(data.pizzas) and check_drinks(data.drinks):
            sum = get_pizza_sum(data.pizzas) + get_drink_sum(data.drinks)

            dpizzas = json.dumps(data.pizzas)
            ddrinks = json.dumps(data.drinks)
            user_data = get_user_number(check)

            discount_data = None

            type = None
            min_s = None
            message = "None"
            sum1 = 0

            if len(data.promocode) > 0:
                z = check_discount(promo=data.promocode, number=user_data)
                if z['status'] == 200:
                    #  Если промокод успешно проверен
                    if z['type'] == 1:
                        type = 1
                        min_s = z['min_sum']
                        sum1 = sum
                        #  Если тип промокода первый
                        if z['min_sum'] > sum:
                            #  Проверка на минимальную сумму
                            return {"status": 460}
                        else:
                            # Если всё нормально, то считаем сумму
                            sum = (sum // 100) * (100 - int(z['discount_data']))
                    elif z['type'] == 2:
                        type = 2
                        min_s = z['min_sum']
                        #  Если тип промокода второй
                        if z['min_sum'] > sum:
                            #  Проверка на минимальную сумму
                            return {"status": 460}
                        else:
                            if sum - int(z['discount_data']) < 0:
                                # Если сумма со скидкой в рублях меньше нуля
                                return {"status": 461}
                            else:
                                sum -= int(z['discount_data'])
                    elif z['type'] == 3:
                        type = 3
                        min_s = z['min_sum']
                        #  Если тип промокода третий
                        if z['min_sum'] > sum:
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

            res_order = set_order(user=user_data, pizzas=dpizzas, drinks=ddrinks, promocode=data.promocode,
                      promocode_item=discount_data,
                      street=data.street, house=data.house, entrance=data.entrance,
                      floor=data.floor, apartment=data.apartment, device=data.device, paytype=data.paytype,
                      price=sum, comment=data.comment, status="accepted", data=time_now.strftime('%Y-%m-%d %H:%M:%S'))

            if len(data.promocode) > 0:
                decrement_promo_count(data.promocode)

            return {"status": 200, "sum": sum, "order_id": res_order}
        else:
            return {"status": 400}
    else:
        return {
            "status": 401,
            "error": "Not valid access token"
        }

@router.get("/api/get/order/{order_id}")
def get_orders(request: Request, order_id: int):
    check = middleware(request.headers.get('authorization'))
    if check is not False:

        user_data = get_user_number(check)
        return {"server_status": 200, "order_info": get_order(id=order_id, number=user_data)}
    else:
        return {"server_status": 400}


@router.post("/api/set/order/backout")
def backout(data: BackoutOrder):
    check = middleware(data.token)
    if check is not False:
        user_data = get_user_number(check)
        return backout_order(id=data.order_id, number=user_data)
    else:
        return {"server_status": 400}

@router.get("/api/get/street")
def get_street():
    return {"streets": get_streets()}

@router.get("/api/get/time")
def get_time():
    time_now = datetime.datetime.now()
    x = time_now.strftime('%H')
    z = None
    if int(x) > 13:
        z = "больше"
    else:
        z = "елсе"
    return {"time": z}


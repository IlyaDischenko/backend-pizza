from fastapi import APIRouter

# from client.users.db_users import add_address, \
#     update_last_active

from client.users.db_users_mongo import get_streets, check_code, exists_user_or_add, add_email, add_name, get_profile_info
from client.orderAndProduct.db_products_mongo import get_all_product

from client.users.model_users import Token, Number, Code, Email, Name
from client.orderAndProduct.models_orderPromo import Promocode
from client.singin.call import call_service
from client.singin.jwt_handler import getJWT, middleware

# from client.orderAndProduct.products_mongo import insert


from client.order.db_order_mongo import add_pizza

router = APIRouter()


@router.get("/")
def null_req():
    return {"all": add_pizza("")}

@router.post("/")
def null_req():
    # insert_promocode(promocode = data.promocode, count = data.count, type = data.type,
    #                  discount_data = data.discount_data, min_sum = data.min_sum, need_number = data.need_number,
    #                  number = data.number, is_view = data.is_view)

    return {"all": "ok"}


@router.get("/get/all/{device}")
def get_pizza(device: str):
    return get_all_product(device)


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
        jwt = getJWT(exists_user_or_add(number=data.number))
        return {
            "status": 200,
            "token": jwt,
        }
    elif not res:
        return {"status": 400}


# # @router.post('/api/token/check')
# # def check_access_token(data: Token):
# #     check = middleware(data.token)
#
# @router.post('/api/refreshtoken')
# def refresh_token(data: Token):
#     try:
#         x = check_refresh(data.token)
#         if x != False:
#             res = getJWT(user_id=x)
#             return {
#                 "access token": res,
#                 # "refresh token": res[1]
#             }
#         else:
#             return {
#                 "status": 401,
#                 "error": "Not valid refresh token"
#             }
#     except:
#         return {"status": 400}
#
#


@router.post("/api/get/userinfo")
def get_user_info_post(token: Token):
    check = middleware(token.token)
    if check:
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
    if check:
        add_result = add_email(id=check, email=data.email)
        # update_last_active(check)
        if add_result:
            return {"status": 200}
        else:
            return {"status": 400}
    elif not check:
        return {
            "status": 401,
            "error": "Not valid access token"
        }


@router.post("/api/set/name")
def set_name(data: Name):
    check = middleware(data.token)
    if check:
        res = add_name(id=check, name=data.name)
        # update_last_active(check)
        if res:
            return {"status": 200}
        else:
            return {"status": 400}
    elif not check:
        return {"status": 401}

# @router.post("/api/set/address")
# def set_address(data: Address):
#     try:
#         check = middleware(data.token)
#         if check != False:
#             add_address(id=check, street=data.street, house=data.house, entrance=data.entrance, floor=data.floor,
#                         apartment=data.apartment)
#             update_last_active(check)
#             return {"status": 200}
#         elif check == False:
#             return {"status": 300}
#     except:
#         return {"status": 200}




#
#
# @router.post("/api/set/order")
# def testPoint(data: Order):
#     check = middleware(data.token)
#     time_now = datetime.datetime.now()
#     tz_moscow = datetime.timedelta(hours=0)
#     fin_time = time_now + tz_moscow
#     x = fin_time.strftime('%H')
#     if int(x) <= 10 or int(x) >= 24:
#         return {"status": 462}
#
#     if check:
#         if check_pizzas(data.pizzas) and check_drinks(data.drinks):
#             sum = get_pizza_sum(data.pizzas) + get_drink_sum(data.drinks)
#
#             dpizzas = json.dumps(data.pizzas)
#             ddrinks = json.dumps(data.drinks)
#             user_data = get_user_number(check)
#
#             discount_data = None
#
#             type = None
#             min_s = None
#             message = "None"
#             sum1 = 0
#
#             if len(data.promocode) > 0:
#                 z = check_discount(promo=data.promocode, number=user_data)
#                 if z['status'] == 200:
#                     #  Если промокод успешно проверен
#                     if z['type'] == 1:
#                         type = 1
#                         min_s = z['min_sum']
#                         sum1 = sum
#                         #  Если тип промокода первый
#                         if z['min_sum'] > sum:
#                             #  Проверка на минимальную сумму
#                             return {"status": 460}
#                         else:
#                             # Если всё нормально, то считаем сумму
#                             sum = (sum // 100) * (100 - int(z['discount_data']))
#                     elif z['type'] == 2:
#                         type = 2
#                         min_s = z['min_sum']
#                         #  Если тип промокода второй
#                         if z['min_sum'] > sum:
#                             #  Проверка на минимальную сумму
#                             return {"status": 460}
#                         else:
#                             if sum - int(z['discount_data']) < 0:
#                                 # Если сумма со скидкой в рублях меньше нуля
#                                 return {"status": 461}
#                             else:
#                                 sum -= int(z['discount_data'])
#                     elif z['type'] == 3:
#                         type = 3
#                         min_s = z['min_sum']
#                         #  Если тип промокода третий
#                         if z['min_sum'] > sum:
#                             #  Проверка на минимальную сумму
#                             return {"status": 460}
#                         else:
#                             discount_data = json.dumps(z['discount_data'])
#                             sum += z['discount_data']['price']
#
#                 elif z['status'] == 400:
#                     return {"status": 450}
#                 elif z['status'] == 401:
#                     return {"status": 451}
#                 elif z['status'] == 422:
#                     return {"status": 452}
#
#             res_order = set_order(user=user_data, pizzas=dpizzas, drinks=ddrinks, promocode=data.promocode,
#                       promocode_item=discount_data,
#                       street=data.street, house=data.house, entrance=data.entrance,
#                       floor=data.floor, apartment=data.apartment, device=data.device, paytype=data.paytype,
#                       price=sum, comment=data.comment, status="accepted", data=time_now.strftime('%Y-%m-%d %H:%M:%S'))
#
#             if len(data.promocode) > 0:
#                 decrement_promo_count(data.promocode)
#
#             return {"status": 200, "sum": sum, "order_id": res_order}
#         else:
#             return {"status": 400}
#     else:
#         return {
#             "status": 401,
#             "error": "Not valid access token"
#         }
#
# @router.get("/api/get/order/{order_id}")
# def get_orders(request: Request, order_id: int):
#     check = middleware(request.headers.get('authorization'))
#     if check is not False:
#
#         user_data = get_user_number(check)
#         return {"server_status": 200, "order_info": get_order(id=order_id, number=user_data)}
#     else:
#         return {"server_status": 400}
#
#
# @router.post("/api/set/order/backout")
# def backout(data: BackoutOrder):
#     check = middleware(data.token)
#     if check is not False:
#         user_data = get_user_number(check)
#         return backout_order(id=data.order_id, number=user_data)
#     else:
#         return {"server_status": 400}
#

@router.get("/api/get/street")
def get_street():
    return {"streets": get_streets()}



#

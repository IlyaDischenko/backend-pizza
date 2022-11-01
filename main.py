from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from users.database_users.db_users import check_code, exists_user_or_add, add_email, add_name, add_address, \
    update_last_active, get_profile_info, get_user_number
from users.database_users.model_users import Token, Number, Code, Email, Name, Address
from users.orderAndProduct.models_orderPromo import Promocode, Insert_promocode, Order
from users.orderAndProduct.products import get_pizzas, get_drinks
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


@app.post("/api/set_order")
def testPoint(data: Order):
    check = middleware(data.token)

    if check:
        dpizzas = json.dumps(data.pizzas)
        ddrinks = json.dumps(data.drinks)
        user_data = get_user_number(check)
        set_order(user=user_data, pizzas=dpizzas, drinks=ddrinks, promocode=data.promocode,
                  street=data.street, house=data.house, entrance=data.entrance,
                  floor=data.floor, apartment=data.apartment, device=data.device, paytype=data.paytype,
                  comment=data.comment, status=data.status)
        return {"data": user_data, "check": check}
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

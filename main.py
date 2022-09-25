from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.database_users.db_users import check_code, exists_user_or_add, add_email, add_name, add_address, update_last_active
from users.database_users.model_users import Token, Number, Code, Email, Name, Address
from users.database_users.products import get_pizzas
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

@app.get("/get")
def get_pizza():
    res = get_pizzas()
    return {"pizza": res}


@app.post("/api/gettoken")
def get_token(num: Number):
    # Функция для отправки номера в сервис и добавление валидного кода в базу
    call_service(num.number)
    return {"status": 200, "number": num.number}


@app.post("/api/confirmtoken")
def confirm_token(data: Code):
    # Функция для проверки кода о получения access токена
    if check_code(number=data.number, code=data.code):
        res = getJWT(exists_user_or_add(number=data.number))
        return {
            "token": res[0],
            "refresh token": res[1]
                }
    elif not check_code(number=data.number, code=data.code):
        return {"status": "Пользователь не найден"}


@app.post('/api/refreshtoken')
def refresh_token(data: Token):
    try:
        x = check_refresh(data.token)
        if x != False:
            res = getJWT(user_id=x)
            return {
                "token": res[0],
                "refresh token": res[1]
                }
        else:
            return {
                "status": 401,
                "error": "Not valid refresh token"
                }
    except:
        return {"error": "Token not valid"}


@app.post("/api/testtoken")
def test_token(token: Token):
    check = middleware(token.token)
    if check != False:
        update_last_active(check)
        return {"payload": check}
    else:
        return {
            "status": 401,
                "error": "Not valid access token"
                }


@app.post("/api/set/email")
def set_email(data: Email):
    try:
        check = middleware(data.token)
        if check != False:
            add_email(id=check, email=data.email)
            update_last_active(check)
            return {"status": "success"}
        elif check == False:
            return {
                "status": 401,
                "error": "Not valid access token"
            }
    except:
        return {"status": "error"}


@app.post("/api/set/name")
def set_name(data: Name):
    try:
        check = middleware(data.token)
        if check != False:
            add_name(id = check, name = data.name)
            update_last_active(check)
            return {"status": "success"}
        elif check == False:
            return {"status": "Not valid token"}
    except:
        return {"status": "error"}


@app.post("/api/set/address")
def set_address(data: Address):
    try:
        check = middleware(data.token)
        if check != False:
            add_address(id=check, street=data.street, house=data.house, entrance=data.entrance, floor=data.floor, apartment=data.apartment)
            update_last_active(check)
            return {"status": "success"}
        elif check == False:
            return {"status": "Not valid token"}
    except:
        return {"status": "error"}

@app.get("/yoyo")
def main():
    return {"status": "okey"}

@app.get("/damir")
def main():
    return {"status": "damir dolboyob"}
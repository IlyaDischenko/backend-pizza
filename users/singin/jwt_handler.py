import time
import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')
JWT_REFRESH_SECRET = config('refresh-secret')


#    Access token
#    Access token
#    Access token
#    Access token
#    Access token

def getJWT(user_id: str):
    # Функция для генерации токена
    payload = {
        "user_id": user_id,
        "expires": time.time() + 2592000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # refreshtoken = jwt.encode(payload, JWT_REFRESH_SECRET, algorithm=JWT_ALGORITHM)

    return token


def middleware(token: bytes):
    # Функция для декодирования токена
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if decode_token["expires"] >= time.time():
            return decode_token['user_id']
        else:
            return False
    except:
        return False


#    Refresh token
#    Refresh token
#    Refresh token
#    Refresh token
#    Refresh token

def check_refresh(token: bytes):
    # Проверка рефреш токена
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if decode_token["expires"] >= time.time():
            return decode_token['user_id']
        else:
            return False
    except:
        return False

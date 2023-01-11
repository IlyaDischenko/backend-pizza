import requests

from users.database_users.db_users import insert_code


def call_service(number):
    # Функция для общения с сервисом телефонии
    payload = {
        "service_id": 424,
        "secret_key": "37c2954f1b3ae5c7fad812280f10795e",
        "phone": number,
        "test": 0
    }

    resp = requests.get('https://api.nerotech.ru/api/v1/call', params=payload).json()

    if resp["status"]:
        # Обработчик в случае успешного ответа
        insert_code(number, resp["code"])
        return {"status": 200}

    elif not resp['status']:
        # Обработчик ошибок в ответах сервиса
        if resp['error'] == 1:
            return {"error": "Неверные параметры.", "code": 1}
        elif resp['error'] == 2:
            return {"error": "Неверный формат номер телефона.", "code": 2}
        elif resp['error'] == 3:
            return {"error": "Неверная комбинация `service_id` и `secret_key`.", "code": 3}
        elif resp['error'] == 4:
            return {"error": "Возникла ошибка при инициализации звонка.", "code": 4}
        elif resp['error'] == 6:
            return {"error": "По данным параметрам ничего не найдено.", "code": 6}
        elif resp['error'] == 7:
            return {"error": "Пополните счёт для звонков.", "code": 7}
        elif resp['error'] == 8:
            return {"error": "Пакет звонков закончился.", "code": 8}
        elif resp['error'] == 9:
            return {"error": "Звонок уже идёт на этот номер.", "code": 9}
        elif resp['error'] == 10:
            return {"error": "Не удалось дозвониться.", "code": 10}
        elif resp['error'] == 11:
            return {"error": "Превышен лимит вызовов на данный номер.", "code": 11}
        elif resp['error'] == 12:
            return {"error": "Номер находится в чёрном списке.", "code": 12}

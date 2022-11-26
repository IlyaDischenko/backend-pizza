from admin import routes as adminRouter
from users import routes as userRouter
from users.Cart import CartRouter as UserCartRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# from users.database_users.db_users import check_code, exists_user_or_add, add_email, add_name, add_address, \
#     update_last_active, get_profile_info, get_user_number, get_streets
# from users.database_users.model_users import Token, Number, Code, Email, Name, Address
# from users.orderAndProduct.models_orderPromo import Promocode, Insert_promocode, Order, GetOrder
# from users.orderAndProduct.products import get_pizzas, get_drinks, check_pizzas, check_drinks, get_drink_sum, \
#     get_pizza_sum
# from users.orderAndProduct.promo import check_discount, insert_json
# from users.orderAndProduct.order import get_order, set_order
# from users.singin.call import call_service
# from users.singin.jwt_handler import getJWT, middleware, check_refresh

app = FastAPI()
app.include_router(adminRouter.router)
app.include_router(userRouter.router)
app.include_router(UserCartRouter.router)

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


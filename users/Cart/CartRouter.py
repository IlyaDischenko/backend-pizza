from fastapi import APIRouter

from users.Cart.CartDB import CartDB

router = APIRouter()

db = CartDB()

@router.get("/cart/add/pizza")
def add_pizza():
    x = db.add_pizza(order_id=1, item_id=4)
    return {"result": x}
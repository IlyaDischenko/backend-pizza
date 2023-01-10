from fastapi import APIRouter

from client.order.db_order_mongo import add_pizza
from client.order.models_orders import AddPizza, AddPromocode
from client.orderAndProduct.db_promo_mongo import add_promocode

router = APIRouter()

@router.post("/add-pizza")
def addPizza(data: AddPizza):
    return add_pizza(item_id=data.item_id, id=data.id)

@router.post("/add-promocode")
def addPromocode(data: AddPromocode):
    return add_promocode(promocode=data.promocode, id=data.id)
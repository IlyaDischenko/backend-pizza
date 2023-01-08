from fastapi import APIRouter

from client.order.db_order_mongo import add_pizza
from client.order.models_orders import AddPizza

router = APIRouter()

@router.post("/add-pizza")
def null_req(data: AddPizza):
    return add_pizza(item_id=data.item_id, id=data.id)
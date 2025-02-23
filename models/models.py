from pydantic import BaseModel
from typing import Optional

"""
The Order class is a Pydantic model that represents the structure of the Order object.
It contains the following attributes:
    - id: An optional integer representing the order ID.
    - symbol: A string representing the order symbol.
    - price: A float representing the order price.
    - quantity: An integer representing the order quantity.
    - order_type: A string representing the type of order.
"""
class Order(BaseModel):
    id: Optional[int] = None
    symbol: str
    price: float
    quantity: int
    order_type: str

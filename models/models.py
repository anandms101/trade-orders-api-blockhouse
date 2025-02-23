from pydantic import BaseModel, field_validator
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

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than zero")
        return v

    @field_validator("symbol")
    @classmethod
    def symbol_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Symbol must not be empty")
        return v.upper() 

    @field_validator("order_type")
    @classmethod
    def order_type_must_be_valid(cls, v):
        v = v.strip()
        allowed = {"buy", "sell"}
        if v.lower() not in allowed:
            raise ValueError(f"order_type must be one of {allowed}")
        return v.lower()
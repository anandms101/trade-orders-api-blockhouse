from fastapi import APIRouter
from typing import List
from models.models import Order
from db.database import get_connection

router = APIRouter()

"""
The read_root function is a FastAPI endpoint that returns a welcome message.
It is accessible at the root URL of the API.
"""
@router.get("/")
def read_root():
    return {"message": "Welcome to the Trade Orders API"}

"""
The get_orders function is a FastAPI endpoint that returns a list of orders from the database.
It is accessible at the '/orders' URL of the API.
The function retrieves the orders from the database and returns them as a list of Order objects.
"""
@router.get("/orders", response_model=List[Order])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symbol, price, quantity, order_type FROM orders")
    orders_data = cursor.fetchall()
    conn.close()
    orders = [ Order(id=row[0], symbol=row[1], price=row[2],
                     quantity=row[3], order_type=row[4]) for row in orders_data ]
    return orders

"""
The create_order function is a FastAPI endpoint that creates a new order in the database.
It is accessible at the '/orders' URL of the API with an HTTP POST request.
The function receives an Order object as input, inserts the order into the database,
and returns the created order with the assigned order ID.
"""
@router.post("/orders", response_model=Order)
def create_order(order: Order):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (symbol, price, quantity, order_type) VALUES (?, ?, ?, ?)",
        (order.symbol, order.price, order.quantity, order.order_type)
    )
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    order.id = order_id
    return order

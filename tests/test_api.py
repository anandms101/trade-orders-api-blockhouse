import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from main import app
from db.database import get_connection 

client = TestClient(app)

def clear_orders_table():
    """
    Utility function to clear the orders table in the database.
    This helps ensure tests run with a clean state.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders")
    conn.commit()
    conn.close()

def test_root():
    """
    Test that the root endpoint returns the expected welcome message.
    This assumes you've defined a GET endpoint at "/" returning:
    {"message": "Welcome to the Trade Orders API"}
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Trade Orders API"}

def test_create_order():
    """
    Test creating an order with valid data.
    Checks that the returned JSON includes the same data plus an assigned 'id'.
    """
    order_data = {
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["symbol"] == order_data["symbol"]
    assert json_data["price"] == order_data["price"]
    assert json_data["quantity"] == order_data["quantity"]
    assert json_data["order_type"] == order_data["order_type"]
    assert "id" in json_data

def test_create_order_missing_field():
    """
    Test that creating an order with a missing required field (symbol) fails.
    The API should return a 422 status code for invalid input.
    """
    order_data = {
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422

def test_create_order_invalid_data():
    """
    Test that creating an order with invalid data types (e.g., price as a string) fails.
    The API should return a 422 status code for invalid input.
    """
    order_data = {
        "symbol": "AAPL",
        "price": "not_a_number",
        "quantity": 10,
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422 

def test_get_orders():
    """
    Test that the GET /orders endpoint returns a list of orders.
    """
    response = client.get("/orders")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)

def test_get_orders_empty():
    """
    Ensure that when there are no orders (by clearing the orders table),
    the GET /orders endpoint returns an empty list.
    """
    clear_orders_table()
    response = client.get("/orders")
    assert response.status_code == 200
    orders = response.json()
    assert orders == []  

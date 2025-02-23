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
    Checks that the returned JSON includes the same data plus an assigned 'id',
    and that the symbol and order_type are normalized.
    """
    clear_orders_table()
    order_data = {
        "symbol": "aapl",            
        "price": 150.0,
        "quantity": 10,
        "order_type": "BUY"          
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["symbol"] == "AAPL"
    assert json_data["price"] == order_data["price"]
    assert json_data["quantity"] == order_data["quantity"]
    assert json_data["order_type"] == "buy"
    assert "id" in json_data

def test_create_order_missing_field():
    """
    Test that creating an order with a missing required field (symbol) fails.
    The API should return a 422 status code for invalid input.
    """
    clear_orders_table()
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
    clear_orders_table()
    order_data = {
        "symbol": "AAPL",
        "price": "not_a_number",
        "quantity": 10,
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422 

def test_create_order_boundary_values():
    """
    Test that orders with boundary values (zero or negative) for price and quantity are rejected.
    """
    clear_orders_table()
    
    order_data_zero = {
        "symbol": "GOOG",
        "price": 0.0,
        "quantity": 0,
        "order_type": "sell"
    }
    response = client.post("/orders", json=order_data_zero)
    assert response.status_code == 422

    order_data_negative = {
        "symbol": "MSFT",
        "price": -100.0,
        "quantity": -5,
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data_negative)
    assert response.status_code == 422

def test_create_multiple_orders():
    """
    Test creating multiple orders and retrieving them.
    """
    clear_orders_table()
    orders_to_create = [
        {"symbol": "AAPL", "price": 150.0, "quantity": 10, "order_type": "buy"},
        {"symbol": "GOOG", "price": 2000.0, "quantity": 5, "order_type": "sell"},
        {"symbol": "TSLA", "price": 700.0, "quantity": 8, "order_type": "buy"}
    ]
    for order in orders_to_create:
        response = client.post("/orders", json=order)
        assert response.status_code == 200

    response = client.get("/orders")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)
    assert len(orders) >= 3

def test_invalid_http_method():
    """
    Test that an invalid HTTP method returns 405.
    For example, sending a PUT request to /orders should not be allowed.
    """
    response = client.put("/orders", json={})
    assert response.status_code == 405

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

def test_duplicate_orders():
    """
    Test that duplicate orders can be created.
    If duplicates are allowed, then the count should increase.
    """
    clear_orders_table()
    order_data = {
        "symbol": "NFLX",
        "price": 500.0,
        "quantity": 15,
        "order_type": "buy"
    }
    response1 = client.post("/orders", json=order_data)
    response2 = client.post("/orders", json=order_data)
    assert response1.status_code == 200
    assert response2.status_code == 200

    response = client.get("/orders")
    orders = response.json()
    nflx_orders = [o for o in orders if o["symbol"] == "NFLX"]
    assert len(nflx_orders) >= 2

def test_websocket():
    """
    Test the WebSocket endpoint.
    Connect to /ws, send a message, and verify the response.
    """
    with client.websocket_connect("/ws") as websocket:
        test_message = "Test order update"
        websocket.send_text(test_message)
        data = websocket.receive_text()
        assert "Order status updated:" in data
        assert test_message in data

def test_symbol_whitespace_normalization():
    """
    Test that the symbol field is trimmed of whitespace and normalized to uppercase.
    """
    clear_orders_table()
    order_data = {
        "symbol": "  msft  ",
        "price": 250.0,
        "quantity": 10,
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["symbol"] == "MSFT"

def test_order_type_whitespace_and_case():
    """
    Test that order_type is normalized even with surrounding whitespace and mixed case.
    """
    clear_orders_table()
    order_data = {
        "symbol": "IBM",
        "price": 130.0,
        "quantity": 10,
        "order_type": "  SeLL  "
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["order_type"] == "sell"

def test_missing_multiple_fields():
    """
    Test that creating an order with multiple missing required fields fails.
    """
    clear_orders_table()
    order_data = {
        "price": 100.0,
        "quantity": 5
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 422

def test_extremely_large_values():
    """
    Test creating an order with extremely large price and quantity values.
    """
    clear_orders_table()
    order_data = {
        "symbol": "BIG",
        "price": 1e12,       
        "quantity": 1000000,  
        "order_type": "buy"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["price"] == order_data["price"]
    assert json_data["quantity"] == order_data["quantity"]

def test_websocket_empty_message():
    """
    Test sending an empty message over the WebSocket endpoint.
    """
    with client.websocket_connect("/ws") as websocket:
        test_message = ""
        websocket.send_text(test_message)
        data = websocket.receive_text()
        assert data
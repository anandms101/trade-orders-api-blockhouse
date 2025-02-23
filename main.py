from fastapi import FastAPI
from routers import orders, websocket

app = FastAPI(title="Trade Orders API", description="A simple API for handling trade orders")

app.include_router(orders.router)
app.include_router(websocket.router)

"""
The main function starts the FastAPI application using Uvicorn.
"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

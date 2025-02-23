from fastapi import APIRouter, WebSocket

router = APIRouter()

"""
The websocket_endpoint function is a FastAPI endpoint that handles WebSocket connections.
It is accessible at the '/ws' URL of the API.
The function accepts WebSocket connections, receives data from the client,
processes the data, and sends a response back to the client.
"""
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Order status updated: {data}")
    except Exception:
        await websocket.close()

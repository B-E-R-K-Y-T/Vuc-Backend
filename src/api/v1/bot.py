import asyncio

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from services.websocket_connector.connector import ConnectionManager
from services.event_system.types import TypeEvent
from services.event_system.event_bus import EventBus

router = APIRouter(
    prefix="/ws",
)
manager = ConnectionManager()


@router.websocket("/tasks")
async def task_handler(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            for event in TypeEvent.fields():
                if EventBus.event_is_exist(event):
                    await EventBus.dispatch(event, websocket=websocket)

            await asyncio.sleep(0.1)

            # if manager.get_active_connections() is None:
            #     break

    except WebSocketDisconnect:
        manager.disconnect(websocket)

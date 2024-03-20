import secrets


async def send_message_user_handler(websocket, telegram_id: int, message: str):
    await websocket.send_text(
            f"id={secrets.token_hex(nbytes=16)},{telegram_id=},{message=}"
    )

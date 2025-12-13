
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app import models, bot, security
import json

router = APIRouter(tags=["chat"])

@router.websocket("/ws/chat")
async def chat_ws(ws: WebSocket, token: str, session_id: int, db: AsyncSession = Depends(get_db)):
    try:
        payload = security.decode_token(token)
    except Exception:
        await ws.close()
        return

    await ws.accept()

    res = await db.execute(select(models.Session).where(models.Session.id == session_id))
    session = res.scalar()
    if not session:
        await ws.close()
        return

    try:
        while True:
            data = json.loads(await ws.receive_text())
            text = data["message"]
            user_msg = models.Message(session_id=session.id, sender="user", text=text)
            db.add(user_msg)
            reply = bot.weather_reply(text)
            bot_msg = models.Message(session_id=session.id, sender="bot", text=reply)
            db.add(bot_msg)
            await db.commit()
            await ws.send_json({"sender": "bot", "text": reply})
    except WebSocketDisconnect:
        pass

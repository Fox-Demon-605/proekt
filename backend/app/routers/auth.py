
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app import models, security
from pydantic import BaseModel, Field

router = APIRouter(prefix="/auth", tags=["auth"])

class UserIn(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=4)

@router.post("/register")
async def register(data: UserIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.User).where(models.User.username == data.username))
    if res.scalar():
        raise HTTPException(400, "User exists")
    user = models.User(username=data.username, password=security.hash_password(data.password))
    db.add(user)
    await db.commit()
    return {"status": "ok"}

@router.post("/login")
async def login(data: UserIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.User).where(models.User.username == data.username))
    user = res.scalar()
    if not user or not security.verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": security.create_token(user.username)}

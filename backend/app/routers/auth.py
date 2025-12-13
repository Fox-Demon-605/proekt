
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app import models, schemas, security

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(data: schemas.UserIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.User).where(models.User.username == data.username))
    if res.scalar():
        raise HTTPException(400, "User exists")
    user = models.User(username=data.username, password=security.hash_password(data.password))
    db.add(user)
    await db.commit()
    return {"status": "ok"}

@router.post("/login", response_model=schemas.Token)
async def login(data: schemas.UserIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.User).where(models.User.username == data.username))
    user = res.scalar()
    if not user or not security.verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": security.create_token(user.username)}

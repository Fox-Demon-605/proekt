
from pydantic import BaseModel, Field
from datetime import datetime

class UserIn(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=4)

class Token(BaseModel):
    access_token: str

class SessionOut(BaseModel):
    id: int
    created_at: datetime

class MessageOut(BaseModel):
    sender: str
    text: str
    created_at: datetime

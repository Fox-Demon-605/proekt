
from passlib.context import CryptContext
import jwt, datetime

SECRET = "CHANGE_ME"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd.hash(p)

def verify_password(p: str, h: str) -> bool:
    return pwd.verify(p, h)

def create_token(username: str):
    return jwt.encode(
        {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
        SECRET,
        algorithm="HS256"
    )

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])

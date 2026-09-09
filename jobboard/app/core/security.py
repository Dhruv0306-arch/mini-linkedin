from fastapi import Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.storage.memory import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    return f"fake-token-for-{user_id}"


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    prefix = "fake-token-for-"
    if not token.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id = int(token.removeprefix(prefix))
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

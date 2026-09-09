from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.user import TokenOut, UserCreate, UserLogin, UserOut
from app.storage.memory import db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate):
    if db.get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = db.create_user(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    return user


@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin):
    user = db.get_user_by_email(payload.email)
    if user is None or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(user["id"])
    return TokenOut(access_token=token)

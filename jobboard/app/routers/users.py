from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.application import ApplicationOut
from app.schemas.user import UserOut
from app.storage.memory import db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/me/applications", response_model=list[ApplicationOut])
def read_my_applications(current_user: dict = Depends(get_current_user)):
    return db.list_applications_for_user(current_user["id"])

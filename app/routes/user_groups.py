from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.crud import crud_user_groups
from ..utils import get_current_user
from ..database import get_db
from .. import schemas, exceptions

router = APIRouter(prefix="/user_groups", tags=["User Groups"])


@router.post("/", response_model=schemas.returnCreatedUserGroup)
def create_user_group(group: schemas.createUserGroup, user: schemas.getUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_user_groups.create_user_group(db, user.id, group)


@router.get("/", response_model=List[schemas.returnCreatedUserGroup])
def get_current_user_user_groups(user: schemas.getUser = Depends(get_current_user), db: Session = Depends(get_db)):
    user_groups = crud_user_groups.get_user_groups(db, user.id)
    if not user_groups:
        raise exceptions.returnNotFound(item="User groups")
    return user_groups
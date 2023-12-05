from typing import Annotated
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.crud import crud_users
from app.utils import get_current_user
from app.database import get_db
from app.schemas import schem_users

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schem_users.ReturnUserDetails)
def create_user_endpoint(user: schem_users.CreateUser, db: Session = Depends(get_db)):
    return crud_users.create_user(db, user)


@router.put("/me/", response_model=schem_users.ReturnUserDetails)
def update_user(updated_user: schem_users.UpdateUser, 
                user: schem_users.GetUser = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    return crud_users.update_user(db, user.id, updated_user)


@router.get("/me/", response_model=schem_users.ReturnCurrentUser)
def get_user_endpoint(user: schem_users.GetUser = Depends(get_current_user)):
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user: schem_users.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    crud_users.delete_user(db, user.id)
    
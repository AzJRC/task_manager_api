from typing import Annotated, List
from fastapi import Body, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.crud import crud_user_groups
from ..utils import get_current_user
from ..database import get_db
from .. import schemas, exceptions

router = APIRouter(prefix="/user_groups", tags=["User Groups"])


@router.post("/", response_model=schemas.returnCreatedUserGroup)
def create_user_group(group: schemas.createUserGroup, user: schemas.getUser = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    return crud_user_groups.create_user_group(db, user.id, group)


@router.get("/", response_model=List[schemas.returnUserGroups]) 
def get_current_user_user_groups(user: schemas.getUser = Depends(get_current_user), 
                                 db: Session = Depends(get_db)):
    user_groups = crud_user_groups.get_current_user_user_groups(db, user.id)
    if not user_groups:
        return []
    return user_groups

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(group_id: int, user: schemas.getUser = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    crud_user_groups.delete_user_group(db, user.id, group_id)


@router.post("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_user_group_member(group_id: int, 
                          group_member: schemas.createUserGroupMember,
                          user: schemas.getUser = Depends(get_current_user), 
                          db: Session = Depends(get_db)):
    crud_user_groups.add_user_group_member(db, user.id, group_id, group_member)
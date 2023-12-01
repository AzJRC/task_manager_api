from typing import Annotated, List
from fastapi import Body, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import exceptions
from app.crud import crud_user_groups
from app.utils import get_current_user
from app.database import get_db
from app.schemas import users_schm, user_groups_schm

router = APIRouter(prefix="/user_groups", tags=["User Groups"])


@router.post("/", response_model=user_groups_schm.ReturnCreatedUserGroup)
def create_user_group(group: user_groups_schm.CreateUserGroup, 
                      user: users_schm.GetUser = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    return crud_user_groups.create_user_group(db, user.id, group)


@router.get("/", response_model=List[user_groups_schm.ReturnUserGroups]) 
def get_current_user_user_groups(user: users_schm.GetUser = Depends(get_current_user), 
                                 db: Session = Depends(get_db)):
    user_groups = crud_user_groups.get_current_user_user_groups(db, user.id)
    if not user_groups:
        return []
    return user_groups


@router.get("/{group_id}/", response_model=user_groups_schm.ReturnUserGroups)
def get_specific_user_group(group_id: str, 
                            user: users_schm.GetUser = Depends(get_current_user), 
                            db: Session = Depends(get_db)):
    if group_id.isdigit():
        return crud_user_groups.get_user_group_by_id(db, user.id, int(group_id))
    else:
        raise exceptions.returnBadRequest(item="User group")

@router.delete("/{group_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(group_id: int, 
                      user: users_schm.GetUser = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    crud_user_groups.delete_user_group(db, user.id, group_id)



# User operations in user groups

@router.post("/{group_id}/members/", status_code=status.HTTP_204_NO_CONTENT)
def add_user_group_member(group_id: int, 
                          group_member: user_groups_schm.CreateUserGroupMember,
                          user: users_schm.GetUser = Depends(get_current_user), 
                          db: Session = Depends(get_db)):
    crud_user_groups.add_user_group_member(db, user.id, group_id, group_member)


# CHAGNES REQUIRED:
# add_user_group_member should return a sucess response


@router.delete("/{group_id}/members/{group_member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group_member(group_id: int,
                             group_member_id: int,
                             user: users_schm.GetUser = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    crud_user_groups.delete_user_group_member(db, user.id, group_id, group_member_id)
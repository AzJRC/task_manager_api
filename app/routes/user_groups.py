from typing import Annotated, List
from fastapi import Body, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import exceptions
from app.crud import crud_user_groups
from app.utils import get_current_user
from app.database import get_db
from app.schemas import schem_users, schem_user_groups

router = APIRouter(prefix="/user_groups", tags=["User Groups"])


@router.post("/", response_model=schem_user_groups.ReturnCreatedUserGroup)
def create_user_group(group: schem_user_groups.CreateUserGroup, 
                      user: schem_users.GetUser = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    return crud_user_groups.create_user_group(db, user.id, group)


@router.get("/", response_model=List[schem_user_groups.ReturnUserGroups]) 
def get_current_user_user_groups(user: schem_users.GetUser = Depends(get_current_user), 
                                 db: Session = Depends(get_db)):
    user_groups = crud_user_groups.get_current_user_user_groups(db, user.id)
    if not user_groups:
        return []
    return user_groups


@router.get("/{group_id}/", response_model=schem_user_groups.ReturnUserGroups)
def get_specific_user_group(group_id: str, 
                            user: schem_users.GetUser = Depends(get_current_user), 
                            db: Session = Depends(get_db)):
    if group_id.isdigit():
        return crud_user_groups.get_user_group_by_id(db, user.id, int(group_id))
    else:
        raise exceptions.returnBadRequest(item="User group")

@router.delete("/{group_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(group_id: int, 
                      user: schem_users.GetUser = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    crud_user_groups.delete_user_group(db, user.id, group_id)



# User operations in user groups | Route: /user_groups/{group_id}/members/...

@router.post("/{group_id}/members/", status_code=status.HTTP_204_NO_CONTENT)
def add_user_group_member(group_id: int, 
                          group_member: schem_user_groups.CreateUserGroupMember,
                          user: schem_users.GetUser = Depends(get_current_user), 
                          db: Session = Depends(get_db)):
    crud_user_groups.add_user_group_member(db, user.id, group_id, group_member)


# ============================================================
# add_user_group_member should return a sucess response
# ============================================================


@router.delete("/{group_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group_member(group_id: int,
                             member_id: int,
                             user: schem_users.GetUser = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    crud_user_groups.delete_user_group_member(db, user.id, group_id, member_id)
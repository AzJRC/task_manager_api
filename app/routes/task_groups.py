from typing import Annotated, List
from fastapi import Body, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import exceptions
from app.crud import crud_taks_groups
from app.utils import get_current_user
from app.database import get_db
from app.schemas import users_schm, task_groups_schm

router = APIRouter(prefix="/task_groups", tags=["Task Groups"])


@router.post("/", response_model=task_groups_schm.ReturnCreatedTaskGroup)
def create_task_group(group: task_groups_schm.CreateTaskGroup, 
                      db: Session = Depends(get_db), 
                      user: users_schm.GetUser = Depends(get_current_user)):
    return crud_taks_groups.create_task_group(db, user.id, group)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_group(group_id: int, 
                      db: Session = Depends(get_db), 
                      user: users_schm.GetUser = Depends(get_current_user)):
    return crud_taks_groups.delete_task_group(db, user.id, group_id)


@router.get("/", response_model=List[task_groups_schm.returnTaskGroup])
def get_current_user_task_groups(db: Session = Depends(get_db), 
                                 user: users_schm.GetUser = Depends(get_current_user)):
    task_groups = crud_taks_groups.get_current_user_task_groups(db, user.id)
    if not task_groups:
        return []
    return task_groups


@router.get("/{group_id}", response_model=task_groups_schm.returnTaskGroup)
def get_specific_task_group(group_id: int, db: Session = Depends(get_db), user: users_schm.GetUser = Depends(get_current_user)):
    return crud_taks_groups.get_specific_task_group(db, user.id, group_id)
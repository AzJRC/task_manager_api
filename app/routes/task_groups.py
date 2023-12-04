from typing import Annotated, List
from fastapi import Body, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import exceptions
from app.crud import crud_taks_groups
from app.utils import get_current_user
from app.database import get_db
from app.schemas import schem_tasks, schem_users, schem_task_groups

router = APIRouter(prefix="/task_groups", tags=["Task Groups"])


@router.post("/", response_model=schem_task_groups.ReturnCreatedTaskGroup)
def create_task_group(group: schem_task_groups.CreateTaskGroup, 
                      db: Session = Depends(get_db), 
                      user: schem_users.GetUser = Depends(get_current_user)):
    return crud_taks_groups.create_task_group(db, user.id, group)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_group(group_id: int, 
                      db: Session = Depends(get_db), 
                      user: schem_users.GetUser = Depends(get_current_user)):
    return crud_taks_groups.delete_task_group(db, user.id, group_id)


@router.get("/", response_model=List[schem_task_groups.returnTaskGroup])
def get_current_user_task_groups(db: Session = Depends(get_db), 
                                 user: schem_users.GetUser = Depends(get_current_user)):
    task_groups = crud_taks_groups.get_current_user_task_groups(db, user.id)
    if not task_groups:
        return []
    return task_groups


@router.get("/{group_id}", response_model=schem_task_groups.returnTaskGroup)
def get_specific_task_group(group_id: int, db: Session = Depends(get_db), user: schem_users.GetUser = Depends(get_current_user)):
    return crud_taks_groups.get_specific_task_group(db, user.id, group_id)


@router.post("/{group_id}/tasks/", response_model=schem_tasks.ReturnUserTask)
def create_task_in_task_group(group_id: int, 
                              task: schem_tasks.CreateTask, 
                              user: schem_users.GetUser = Depends(get_current_user), 
                              db: Session = Depends(get_db)):
    return crud_taks_groups.create_task_in_task_group(db, user.id, group_id, task)



@router.get("/{group_id}/tasks/", response_model=List[schem_tasks.ReturnUserTask])
def get_tasks_in_task_group(group_id: int, 
                            user: schem_users.GetUser = Depends(get_current_user), 
                            db: Session = Depends(get_db)):
    return crud_taks_groups.get_tasks_in_task_group(db, user.id, group_id)


@router.get("/{group_id}/tasks/{task_id}/", response_model=schem_tasks.ReturnUserTask)
def get_specific_task_in_task_group(group_id: int, 
                                    task_id: int, 
                                    user: schem_users.GetUser = Depends(get_current_user), 
                                    db: Session = Depends(get_db)):
    return crud_taks_groups.get_specific_task_in_task_group(db, user.id, group_id, task_id)




@router.delete("/{group_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task_from_task_group(group_id: int, 
                                task_id: int, 
                                user: schem_users.GetUser = Depends(get_current_user), 
                                db: Session = Depends(get_db)):
    crud_taks_groups.remove_task_from_task_group(db, user.id, group_id, task_id)
from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from app.crud import crud_tasks
from app.utils import get_current_user
from app.database import get_db
from app.schemas import schem_tasks, schem_users, schem_task_groups
from app import exceptions

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schem_tasks.ReturnUserTask)
def create_task(task: schem_tasks.CreateTask, user: schem_users.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tasks.create_task(db, user.id, task)


@router.get("/", response_model=List[schem_tasks.ReturnUserTask])
def get_current_user_tasks(title: str = "", description: str = "", user: schem_users.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tasks.get_current_user_tasks(db, user.id, title, description)


@router.get("/{task_id}/", response_model=schem_tasks.ReturnUserTask)
def get_task_by_id(task_id: str, user: schem_users.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    task = crud_tasks.get_task_by_id(db, user.id, int(task_id))
    if not task:
        raise exceptions.returnNotFound(item="Task")
    return task


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id(task_id: str, user: schem_users.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    crud_tasks.delete_task_by_id(db, user.id, int(task_id))


@router.post("/{task_id}/task_groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def assign_task_to_task_group(task_id: int, 
                              group_id: int, 
                              user: schem_users.GetUser = Depends(get_current_user), 
                              db: Session = Depends(get_db)):
    crud_tasks.assign_task_to_task_group(db, user.id, task_id, group_id)
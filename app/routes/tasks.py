from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from app.crud import crud_tasks
from app.utils import get_current_user
from app.database import get_db
from app.schemas import tasks_schm, users_schm
from app import exceptions

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=tasks_schm.ReturnUserTask)
def create_task_endpoint(task: tasks_schm.CreateTask, user: users_schm.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tasks.create_task(db, user.id, task)


@router.get("/", response_model=List[tasks_schm.ReturnUserTask])
def get_user_tasks(title: str = "", description: str = "", user: users_schm.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tasks.get_current_user_tasks(db, user.id, title, description)


@router.get("/{id}/", response_model=tasks_schm.ReturnUserTask)
def get_specific_user_task(id: str, user: users_schm.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    task = crud_tasks.get_task_by_id(db, user.id, int(id))
    if not task:
        raise exceptions.returnNotFound(item="Task")
    return task


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: str, user: users_schm.GetUser = Depends(get_current_user), db: Session = Depends(get_db)):
    crud_tasks.delete_task_by_id(db, user.id, int(id))
    
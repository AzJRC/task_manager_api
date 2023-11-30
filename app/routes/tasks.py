from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.crud import crud_tasks
from ..utils import get_current_user
from ..database import get_db
from .. import schemas, exceptions

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.returnUserTask)
def create_task_endpoint(task: schemas.createTask, user: schemas.getUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tasks.create_task(db, user.id, task)


@router.get("/", response_model=List[schemas.returnUserTask])
def get_user_tasks(title: str = "", description: str = "", user: schemas.getUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_tasks.get_current_user_tasks(db, user.id, title, description)


@router.get("/{id_title}", response_model=schemas.returnUserTask)
def get_specific_user_task(id_title: str, user: schemas.getUser = Depends(get_current_user), db: Session = Depends(get_db)):
    if id_title.isdigit():
        task = crud_tasks.get_task_by_id(db, user.id, int(id_title))
    else:
        task = crud_tasks.get_task_by_title(db, user.id, id_title)
    if not task:
        raise exceptions.returnNotFound(item="Task")
    return task
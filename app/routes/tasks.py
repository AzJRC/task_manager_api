from typing import Annotated
from psycopg2 import IntegrityError
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..utils import get_current_user
from .. import models, schemas, database

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.returnTask)
def get_tasks(task: schemas.createTask, user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    print(user.id)
    new_task = models.TasksTable(title=task.title, description=task.description, task_owner_id=user.id)
    db.add(new_task)
    try:
        db.commit()
        pass
    except Exception as e:
        print(e)
        db.rollback()
        if isinstance(e, IntegrityError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Task already exists.")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        db.refresh(new_task)
        return new_task
    

@router.get("/", response_model=list[schemas.returnUserTask])
def get_user_tasks(user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    task_list = db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user.id).all()
    return task_list


@router.get("/{id}", response_model=schemas.returnUserTask)
def get_user_tasks_by_id(id: int, user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    task_list = db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user.id, models.TasksTable.id == id).one_or_none()
    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return task_list


@router.get("/{title}", response_model=schemas.returnUserTask)
def get_user_tasks_by_title(title: str, user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    task_list = db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user.id, models.TasksTable.title == title).one_or_none()
    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return task_list

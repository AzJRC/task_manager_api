from typing import Annotated
from psycopg2 import IntegrityError
from enum import Enum
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..utils import get_current_user, get_title_standard
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
def get_user_tasks(title: str = "", description: str = "", user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if title or description:
        title_like = "%{}%".format(title)
        description_like = "%{}%".format(description)
        task_list = db.query(models.TasksTable).\
            filter(models.TasksTable.task_owner_id == user.id, 
                   models.TasksTable.title.like(title_like),
                   models.TasksTable.description.like(description_like)).all()
    else:
        task_list = db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user.id).all()
    return task_list


@router.get("/{id_title}", response_model=schemas.returnUserTask)
def get_user_tasks_by_id(id_title: str, user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if id_title.isdigit():
        task_list = db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user.id, models.TasksTable.id == id_title).one_or_none()
    else:
        title = get_title_standard(id_title) #replaces underscores with spaces
        task_list = db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user.id, models.TasksTable.title == title).one_or_none()
    if not task_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return task_list

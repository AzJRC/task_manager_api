from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from .. import models, schemas, exceptions


def create_task(db: Session,  user_id: int, task: schemas.createTask):
    new_task = models.TasksTable(title=task.title, description=task.description, task_owner_id=user_id)
    db.add(new_task)
    try:
        db.commit()
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Task")
        print(e)
        db.rollback()
        raise exceptions.returnUnknownError()
    else:
        db.refresh(new_task)
        return new_task


def get_current_user_tasks(db: Session, user_id: int, title: str, description: str):
    return db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user_id,
                                              models.TasksTable.title.like("%{}%".format(title)),
                                              models.TasksTable.description.like("%{}%".format(description))).all()


def get_task_by_id(db: Session, user_id: int, task_id: int):
    return db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user_id, 
                                              models.TasksTable.id == task_id).one_or_none()


def get_task_by_title(db: Session, user_id: int, task_title: str):
    return db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user_id, 
                                              models.TasksTable.title == task_title).one_or_none()


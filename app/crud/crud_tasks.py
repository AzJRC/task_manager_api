from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import models, exceptions
from app.schemas import tasks_schm

def create_task(db: Session,  user_id: int, task: tasks_schm.CreateTask):
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


def delete_task_by_id(db: Session, user_id: int, task_id: int):
    db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user_id, 
                                       models.TasksTable.id == task_id).delete()
    db.commit()



def get_task_by_id(db: Session, user_id: int, task_id: int):
    return db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user_id, 
                                              models.TasksTable.id == task_id).one_or_none()



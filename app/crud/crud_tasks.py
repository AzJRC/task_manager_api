from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, exceptions
from app.crud import crud_taks_groups
from app.schemas import schem_tasks, schem_task_groups

def create_task(db: Session,  user_id: int, task: schem_tasks.CreateTask):
    new_task = models.TasksTable(title=task.title, description=task.description, task_owner_id=user_id)
    db.add(new_task)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Task")
        print(e)
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


def update_task(db: Session, user_id: int, task_id: int, task: schem_tasks.UpdateTask):
    task_to_update = db.query(models.TasksTable).filter(models.TasksTable.id == task_id, 
                                       models.TasksTable.task_owner_id == user_id).one_or_none()
    if not task_to_update:
        raise exceptions.returnNotFound(item="Task")
    task_to_update.title = task.title
    task_to_update.description = task.description
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise exceptions.returnUnknownError()
    return task_to_update


def delete_task_by_id(db: Session, user_id: int, task_id: int):
    db.query(models.TasksTable).filter(models.TasksTable.task_owner_id == user_id, 
                                       models.TasksTable.id == task_id).delete()
    db.commit()


# ===================================
# TASK GROUP ACTIONS IN TASK ENDPOINT
# ===================================


def assign_task_to_task_group(db: Session, user_id: int, task_id: int, task_group_id: int):
    #verify you are the owner of the task_group and the task
    task = get_task_by_id(db, user_id, task_id)
    if not task:
        raise exceptions.returnNotFound("Task")
    task_group = crud_taks_groups.get_specific_task_group(db, user_id, task_group_id)
    if not task_group:
        raise exceptions.returnNotFound("Task group")
    new_task_assignment = models.TaskAssignmentsAssociationTable(task_id=task_id, task_group_id=task_group_id)
    db.add(new_task_assignment)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Task")
        print(e)
        raise exceptions.returnUnknownError()
    else:
        db.refresh(new_task_assignment)

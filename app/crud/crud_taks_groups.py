from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import exceptions, models
from app.schemas import task_groups_schm


def create_task_group(db: Session, user_id: int, task_group: task_groups_schm.CreateTaskGroup):
    new_task_group = models.TaskGroupsTable(group_name=task_group.group_name, 
                                            group_description=task_group.group_description, 
                                            group_owner_id=user_id)
    db.add(new_task_group)
    try:
        db.commit()
    except Exception as e:
        print(e)
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="User group")
        print(e)
        db.rollback()
        raise exceptions.returnUnknownError()
    else:
        db.refresh(new_task_group)
        return new_task_group
    

def delete_task_group(db: Session, user_id: int, task_group_id: int):
    task_group = db.query(models.TaskGroupsTable).\
        filter(models.TaskGroupsTable.id == task_group_id, models.TaskGroupsTable.group_owner_id == user_id).delete()
    if not task_group:
        raise exceptions.returnNotFound(item="Task group")
    db.commit()


def get_current_user_task_groups(db: Session, user_id: int):
    task_groups = db.query(models.TaskGroupsTable).filter(models.TaskGroupsTable.group_owner_id == user_id).all()
    for task_group in task_groups:
        tasks = db.query(models.TasksTable.id, models.TasksTable.title).\
            join(models.TaskAssignmentsAssociationTable, models.TaskAssignmentsAssociationTable.task_id == models.TasksTable.id).\
            filter(models.TaskAssignmentsAssociationTable.task_group_id == task_group.id).all()
        task_group.tasks = tasks
    return task_groups


def get_specific_task_group(db: Session, user_id: int, task_group_id: int):
    task_group = db.query(models.TaskGroupsTable).\
        filter(models.TaskGroupsTable.group_owner_id == user_id, models.TaskGroupsTable.id == task_group_id).one_or_none()
    if not task_group:
        raise exceptions.returnNotFound(item="Task group")
    return task_group

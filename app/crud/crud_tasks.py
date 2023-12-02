from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import models, exceptions
from app.schemas import tasks_schm, task_groups_schm

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


def assign_task_task_group(db: Session, user_id: int, task_id: int, task_group: task_groups_schm.assignTaskToTaskGroup):
    if not task_group.group_id:
        search_task_group = db.query(models.TaskGroupsTable).\
            filter(models.TaskGroupsTable.group_owner_id == task_group.group_owner_id,
                   models.TaskGroupsTable.group_name == task_group.group_name).one_or_none()
        if not search_task_group:
            raise exceptions.returnNotFound("Task group")
        task_group.group_id = search_task_group.id
    new_task_assignment = models.TaskAssignmentsAssociationTable(task_id=task_id, task_group_id=task_group.group_id)
    db.add(new_task_assignment)
    try:
        db.commit()
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Task assignment")
        print(e)
        db.rollback()
        raise exceptions.returnUnknownError()
    else:
        db.refresh(new_task_assignment)
        return new_task_assignment
    

def delete_task_task_group_assignment(db: Session, user_id: int, task_id: int, task_group_id: int):
    task_assignment = db.query(models.TaskAssignmentsAssociationTable,
             models.TaskGroupsTable.group_owner_id).\
        join(models.TaskGroupsTable, models.TaskGroupsTable.id == task_group_id).\
        filter(models.TaskAssignmentsAssociationTable.task_id == task_id,
               models.TaskAssignmentsAssociationTable.task_group_id == task_group_id,
               models.TaskGroupsTable.group_owner_id == user_id).one_or_none()
    if not task_assignment:
        raise exceptions.returnNotFound("Task assignment")
    db.query(models.TaskAssignmentsAssociationTable).\
        filter(models.TaskAssignmentsAssociationTable.task_id == task_id,
               models.TaskAssignmentsAssociationTable.task_group_id == task_group_id).delete()
    db.commit()
    
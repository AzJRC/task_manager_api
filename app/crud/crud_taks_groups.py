from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import exceptions, models
from app.schemas import schem_task_groups, schem_tasks
from app.crud import crud_tasks


def create_task_group(db: Session, user_id: int, task_group: schem_task_groups.CreateTaskGroup):
    new_task_group = models.TaskGroupsTable(group_name=task_group.group_name, 
                                            group_description=task_group.group_description, 
                                            group_owner_id=user_id)
    db.add(new_task_group)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="User group")
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
    tasks = db.query(models.TasksTable.id, models.TasksTable.title).\
            join(models.TaskAssignmentsAssociationTable, models.TaskAssignmentsAssociationTable.task_id == models.TasksTable.id).\
            filter(models.TaskAssignmentsAssociationTable.task_group_id == task_group.id).all()
    task_group.tasks = tasks
    return task_group


def create_task_in_task_group(db: Session, user_id: int, task_group_id: int, task: schem_tasks.CreateTask):
    if not get_specific_task_group(db, user_id, task_group_id):
        raise exceptions.returnNotFound("Task group")
    new_task = crud_tasks.create_task(db, user_id, task) # function in crud_tasks.py
    new_task_assignment = models.TaskAssignmentsAssociationTable(task_id=new_task.id, task_group_id=task_group_id)
    db.add(new_task_assignment)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Task assignment")
        raise exceptions.returnUnknownError()
    else:
        db.refresh(new_task_assignment)
        return new_task
    

def get_tasks_in_task_group(db: Session, user_id: int, task_group_id: int):
    return db.query(models.TasksTable).\
        join(models.TaskAssignmentsAssociationTable, models.TaskAssignmentsAssociationTable.task_id == models.TasksTable.id).\
        filter(models.TasksTable.task_owner_id == user_id, models.TaskAssignmentsAssociationTable.task_group_id == task_group_id).all()


def get_specific_task_in_task_group(db: Session, user_id: int, task_group_id: int, task_id: int):
    task = db.query(models.TasksTable).\
        join(models.TaskAssignmentsAssociationTable, models.TaskAssignmentsAssociationTable.task_id == models.TasksTable.id).\
        filter(models.TasksTable.task_owner_id == user_id, 
               models.TaskAssignmentsAssociationTable.task_group_id == task_group_id,
               models.TaskAssignmentsAssociationTable.task_id == task_id).one_or_none()
    if not task:
        raise exceptions.returnNotFound(item="Task")
    return task


def remove_task_from_task_group(db: Session, user_id: int, task_group_id: int, task_id: int):
    task_group = get_specific_task_group(db, user_id, task_group_id)
    if not task_group:
        raise exceptions.returnNotFound("Task group")
    task_to_remove = db.query(models.TaskAssignmentsAssociationTable).filter(models.TaskAssignmentsAssociationTable.task_group_id == task_group_id,
                                                            models.TaskAssignmentsAssociationTable.task_id == task_id).delete()
    if not task_to_remove:
        raise exceptions.returnNotFound(item="Task in group")
    db.commit()

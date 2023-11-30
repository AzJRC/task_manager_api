from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from .. import models, schemas, exceptions

def create_user_group(db: Session, user_id: int, user_group: schemas.createUserGroup):
    new_user_group = models.UserGroupsTable(group_name=user_group.group_name, 
                                            group_description=user_group.group_description, 
                                            group_owner_id=user_id)
    db.add(new_user_group)
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
        db.refresh(new_user_group)
        return new_user_group
    

def get_user_groups(db: Session, user_id: int):
    return db.query(models.UserGroupsTable).filter(models.UserGroupsTable.group_owner_id == user_id).all()
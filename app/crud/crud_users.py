from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils import get_password_hash
from app import models, exceptions
from app.schemas import schem_users


def create_user(db: Session, user: schem_users.CreateUser):
    hashed_password = get_password_hash(user.password)
    new_user = models.UsersTable(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Task")
        print(e)
        raise exceptions.returnUnknownError()
    else:
        db.refresh(new_user)
        user_details = schem_users.GetUser(username=new_user.username, email=new_user.email, user_state=new_user.user_state)
        return schem_users.ReturnUserDetails(operation="successful", user_details=user_details)


def get_user(db: Session, user_id: int):
    return db.query(models.UsersTable).filter(models.UsersTable.id == user_id).first()


def update_user(db: Session, user_id: int, updated_user: schem_users.UpdateUser):
    user = db.query(models.UsersTable).filter(models.UsersTable.id == user_id).one_or_none()
    if not user:
        raise exceptions.returnUnknownError()
    user.username = updated_user.username
    user.password = get_password_hash(updated_user.password)
    user.email = updated_user.email
    user.valid_email = False
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise exceptions.returnUnknownError()
    user_details = schem_users.GetUser(username=user.username, email=user.email, user_state=user.user_state)
    return schem_users.ReturnUserDetails(operation="successful", user_details=user_details)


def delete_user(db: Session, user_id: int):
    db.query(models.UsersTable).filter(models.UsersTable.id == user_id).delete()
    db.commit()
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils import get_password_hash
from app import models
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
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="User already exists.")
        print(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "An unexpected error occurred.")
    else:
        db.refresh(new_user)
        user_details = schem_users.GetUser(username=new_user.username, email=new_user.email, user_state=new_user.user_state)
        return schem_users.ReturnUserDetails(operation="successful", user_details=user_details)


def get_user(db: Session, user_id: int):
    return db.query(models.UsersTable).filter(models.UsersTable.id == user_id).first()


def delete_user(db: Session, user_id: int):
    db.query(models.UsersTable).filter(models.UsersTable.id == user_id).delete()
    db.commit()
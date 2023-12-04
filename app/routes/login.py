from datetime import timedelta
from typing import Annotated
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.utils import verify_password
from app.schemas import schem_login
from app import models, database

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/", response_model=schem_login.ReturnToken)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.UsersTable.username, models.UsersTable.email, models.UsersTable.password).\
        filter(models.UsersTable.username == form_data.username).one_or_none()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "0dbf624c8cbfa904ce68120b7099edc65b6405ecaed81850704efbb7bd8673e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




from typing import Annotated
from psycopg2 import IntegrityError
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..auth import oauth2_scheme
from ..utils import get_current_user, get_password_hash
from .. import models, schemas, database

router = APIRouter(prefix="/tasks", tags=["Tasks"])
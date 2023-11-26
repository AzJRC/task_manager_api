from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from .database import Base


class UsersTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    valid_email = Column(Boolean, nullable=False, server_default=text("FALSE")) # email validation
    user_state = Column(Boolean, nullable=False, server_default=text("TRUE")) # user_state -> True: Active, False: Inactive (For irreversible user deletion)

    tasks = relationship("TasksTable", back_populates="users")


class TasksTable(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("TRUE"))
    creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    task_owner = Column(Integer, ForeignKey("users.id"), nullable=False)

    users = relationship("UsersTable", back_populates="tasks")


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, text, Enum
from sqlalchemy.orm import relationship, declarative_base
from .database import Base


dec_base = declarative_base()


# Association tables


group_roles = Table("group_roles", Base.metadata,
                    Column("id", Integer, primary_key=True),
                    Column("role", String, nullable=False)) 


user_group_members = Table("user_group_members", Base.metadata, 
                           Column("user_id", Integer, ForeignKey("users.id"), primary_key=True), 
                           Column("group_id", Integer, ForeignKey("user_groups.id"), primary_key=True),
                           Column("role_id", Integer, ForeignKey("group_roles.id"), nullable=False))


# Main tables
class UsersTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    valid_email = Column(Boolean, nullable=False, server_default=text("FALSE"))  # email validation # user_state -> True: Active, False: Inactive (For irreversible user deletion)
    user_state = Column(Boolean, nullable=False, server_default=text("TRUE"))

    tasks = relationship("TasksTable", back_populates="task_owner") 
    user_group = relationship("UserGroupsTable", back_populates="user_group_owner")
    task_group = relationship("TaskGroupsTable", back_populates="task_group_owner")
    
    #secondary relationships
    group_member = relationship("UserGroupsTable", secondary=user_group_members, back_populates="members")


class UserGroupsTable(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False, unique=True)
    group_description = Column(String, nullable=True)
    group_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    group_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_group_owner = relationship("UsersTable", back_populates="user_group")
    
    #secondary relationships
    members = relationship("UsersTable", secondary=user_group_members, back_populates="group_member")


class TasksTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    task_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    task_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task_owner = relationship("UsersTable", back_populates="tasks")


class TaskGroupsTable(Base):
    __tablename__ = "task_groups" 

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False, unique=True)
    group_description = Column(String, nullable=True)
    group_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    group_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task_group_owner = relationship("UsersTable", back_populates="task_group")
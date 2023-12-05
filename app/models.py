from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint, text, Enum, event
from sqlalchemy.orm import relationship
from .database import Base


# Association tables
class TaskAssignmentsAssociationTable(Base):
    __tablename__ = "task_assignments"

    task_id = Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    task_group_id = Column("task_group_id", Integer, ForeignKey("task_groups.id", ondelete="CASCADE"), primary_key=True)

    tasks = relationship("TasksTable", back_populates="assigned_task_groups")
    task_groups = relationship("TaskGroupsTable", back_populates="assigned_tasks")


# Main tables

delete_children_cascade="all, delete-orphan"
class UsersTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    valid_email = Column(Boolean, nullable=False, server_default=text("FALSE"))  # email validation # user_state -> True: Active, False: Inactive (For irreversible user deletion)
    user_state = Column(Boolean, nullable=False, server_default=text("TRUE"))

    groups_member = relationship("UserGroupMembersAssociationTable", back_populates="member", cascade=delete_children_cascade)
    owned_task_groups = relationship("TaskGroupsTable", back_populates="group_owner", cascade=delete_children_cascade)
    owned_tasks = relationship("TasksTable", back_populates="task_owner", cascade=delete_children_cascade) 


class TasksTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    task_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    task_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    task_owner = relationship("UsersTable", back_populates="owned_tasks")
    assigned_task_groups = relationship("TaskAssignmentsAssociationTable", back_populates="tasks", cascade=delete_children_cascade)
    

    __table_args__ = (
        UniqueConstraint('task_owner_id', 'title'),
    )


class TaskGroupsTable(Base):
    __tablename__ = "task_groups" 

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    group_description = Column(String, nullable=True)
    group_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    group_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    group_owner = relationship("UsersTable", back_populates="owned_task_groups")
    assigned_tasks = relationship("TaskAssignmentsAssociationTable", back_populates="task_groups", cascade=delete_children_cascade)
    

    __table_args__ = (
        UniqueConstraint('group_owner_id', 'group_name'),
    )
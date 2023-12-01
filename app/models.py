from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, text, Enum, event
from sqlalchemy.orm import relationship, declarative_base
from .database import Base


task_assignments = Table("task_assignments", Base.metadata,
                         Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
                         Column("task_group_id", Integer, ForeignKey("task_groups.id", ondelete="CASCADE"), primary_key=True))


user_groups_task_groups = Table("user_groups_task_groups", Base.metadata, 
                                Column("user_group_id", Integer, ForeignKey("user_groups.id", ondelete="CASCADE"), primary_key=True),
                                Column("task_group_id", Integer, ForeignKey("task_groups.id", ondelete="CASCADE"), primary_key=True))

class GroupRoles(Base):
    __tablename__ = "user_group_roles"
    
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)

    user = relationship("UserGroupMembersAssociationTable", back_populates="user_role")

class UserGroupMembersAssociationTable(Base):
    __tablename__ = "user_group_members"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    group_id = Column(Integer, ForeignKey("user_groups.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("user_group_roles.id", ondelete="CASCADE"), nullable=False, server_default=text("1"))

    member = relationship("UsersTable", back_populates="groups_member")
    user_group = relationship("UserGroupsTable", back_populates="members")
    user_role = relationship("GroupRoles", back_populates="user")


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

    owned_user_groups = relationship("UserGroupsTable", back_populates="group_owner", cascade=delete_children_cascade)
    groups_member = relationship("UserGroupMembersAssociationTable", back_populates="member", cascade=delete_children_cascade)
    owned_task_groups = relationship("TaskGroupsTable", back_populates="group_owner", cascade=delete_children_cascade)
    owned_tasks = relationship("TasksTable", back_populates="task_owner", cascade=delete_children_cascade) 


class UserGroupsTable(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    group_description = Column(String, nullable=True)
    group_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    group_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    group_owner = relationship("UsersTable", back_populates="owned_user_groups")
    members = relationship("UserGroupMembersAssociationTable", back_populates="user_group")
    
    #secondary relationships
    assigned_task_groups = relationship("TaskGroupsTable", secondary=user_groups_task_groups, back_populates="assigned_user_groups")


class TasksTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    task_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    task_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    task_owner = relationship("UsersTable", back_populates="owned_tasks")
    assigned_task_groups = relationship("TaskGroupsTable", secondary=task_assignments, back_populates="assigned_tasks")


class TaskGroupsTable(Base):
    __tablename__ = "task_groups" 

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    group_description = Column(String, nullable=True)
    group_creation = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    group_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    group_owner = relationship("UsersTable", back_populates="owned_task_groups")
    assigned_user_groups = relationship("UserGroupsTable", secondary=user_groups_task_groups, back_populates="assigned_task_groups")
    assigned_tasks = relationship("TasksTable", secondary=task_assignments, back_populates="assigned_task_groups")
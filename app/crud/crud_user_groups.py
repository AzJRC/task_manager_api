from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status
from app import models, schemas, exceptions
from app.database import get_db
from app.schemas import user_groups_schm
from . import crud_users


def get_role_id(db: Session, role: str):
    role = db.query(models.GroupRoles).filter(models.GroupRoles.role == role).one_or_none()
    if not role:
        raise exceptions.returnNotFound(item="Role")
    return role.id


def create_user_group(db: Session, user_id: int, user_group: user_groups_schm.CreateUserGroup):
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
        # add current user as the owner of the group
        add_user_group_member(db, user_id, new_user_group.id, 
                              user_groups_schm.CreateUserGroupMember(member_id=user_id, member_role=get_role_id(db, "owner")))
        return new_user_group
    

def get_current_user_user_groups(db: Session, user_id: int):
    user_groups = db.query(models.UserGroupsTable).filter(models.UserGroupsTable.group_owner_id == user_id).all()
    for user_group in user_groups:
        group_members = db.query(models.UsersTable.username, models.GroupRoles.role).\
            join(models.UserGroupMembersAssociationTable, models.UserGroupMembersAssociationTable.user_id == models.UsersTable.id).\
            join(models.GroupRoles, models.GroupRoles.id == models.UserGroupMembersAssociationTable.role_id).\
            filter(models.UserGroupMembersAssociationTable.group_id == user_group.id).all()
        user_group.members_list = group_members
    return user_groups


def get_user_group_by_id(db: Session, user_id: int, group_id: int):
    user_group = db.query(models.UserGroupsTable).\
        filter(models.UserGroupsTable.group_owner_id == user_id,
               models.UserGroupsTable.id == group_id).one_or_none()
    if not user_group:
        raise exceptions.returnNotFound(item="User group")
    group_members = db.query(models.UsersTable.username, models.GroupRoles.role).\
        join(models.UserGroupMembersAssociationTable, models.UserGroupMembersAssociationTable.user_id == models.UsersTable.id).\
        join(models.GroupRoles, models.GroupRoles.id == models.UserGroupMembersAssociationTable.role_id).\
        filter(models.UserGroupMembersAssociationTable.group_id == user_group.id).all()
    user_group.members_list = group_members
    return user_group


# # =================================================== 
# # Note:
# # group_members query is duplicated.
# # Create another function to aviod repetition
# # ===================================================

def delete_user_group(db: Session, user_id: int, group_id: int):
    db.query(models.UserGroupsTable).filter(models.UserGroupsTable.group_owner_id == user_id,
                                            models.UserGroupsTable.id == group_id).delete()
    db.commit()


def add_user_group_member(db: Session, user_id: int, group_id: int, group_member: user_groups_schm.CreateUserGroupMember):
    # Verify that your group exists and you are the owner
    user_group = db.query(models.UserGroupsTable).\
        filter(models.UserGroupsTable.id == group_id, models.UserGroupsTable.group_owner_id == user_id).one_or_none()
    if not user_group:
        raise exceptions.returnNotFound(item="User group")
    #verify user member exists
    new_member = crud_users.get_user(db, group_member.member_id)
    if not new_member:
        raise exceptions.returnNotFound(item="User")
    #Add member to the association table
    user_group_member = models.UserGroupMembersAssociationTable(user_id=new_member.id, group_id=group_id, role_id=group_member.member_role)
    db.add(user_group_member)
    try:
        db.commit()
    except Exception as e:
        print(e)
        if isinstance(e, IntegrityError):
            raise exceptions.returnIntegrityError(item="Group member")
        print(e)
        db.rollback()
        raise exceptions.returnUnknownError()
    else:
        db.refresh(user_group_member)
        return user_group_member
    

def delete_user_group_member(db: Session, user_id: int, group_id: int, group_member_id: int):
    user_group = db.query(models.UserGroupsTable).\
        filter(models.UserGroupsTable.id == group_id, models.UserGroupsTable.group_owner_id == user_id).one_or_none()
    if not user_group:
        raise exceptions.returnNotFound(item="User group")
    entry = db.query(models.UserGroupMembersAssociationTable).\
        filter(models.UserGroupMembersAssociationTable.user_id == group_member_id, 
               models.UserGroupMembersAssociationTable.group_id == group_id).delete()
    db.commit()

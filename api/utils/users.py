from sqlalchemy import text
from fastapi import HTTPException, status

from db.models.hotels import (
    User,
    UserInfo,
    Address
)


def users_list(session_local):
    # user_list =[]
    # result = session_local.query(User).order_by(User.id.asc()).all()
    # for row in result:
    #     user_list.append({"id": row.id, "username": row.user_name, "created at": row.created_at})

    user_list = session_local.query(User).from_statement(text("SELECT users.id, users.user_name, users.created_at FROM users")).all()

    return user_list


def user_detail(username, session_local):
    user = session_local.query(User).filter_by(user_name=username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    info = session_local.query(UserInfo).filter_by(user_id=user.id).first()
    addr = session_local.query(Address).filter_by(user_id=user.id).first()
    return info, addr

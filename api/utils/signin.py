from fastapi import HTTPException, status

from db.models.hotels import (
    User
)



def sign_in(
        user_name, 
        password,
        session_local
        ):
    session = session_local

    username_check = session.query(User).filter_by(user_name=user_name).first()
    if not username_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong username or password"
        )
    if password != username_check.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong username or password"
        )

    return {"message": f"Welcome {user_name}"}

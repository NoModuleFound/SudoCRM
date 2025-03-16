# from backend.api.schemas.user_schema import *

from backend.shared.db.models import *
from backend.api.schemas.users_schema import CreateUser, LoginUser
from backend.api.schemas.system_schema import ApiResponse
# from backend.api.schemas.system_schema import *
from fastapi import status
from backend.shared.db.database import async_session_factory

from backend.shared.utils.auth_module import AuthManagement

from fastapi import HTTPException

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
# from backend.shared.misc.auth_utils import encode_jwt

async def create_new_user(userdata: CreateUser):
    async with async_session_factory() as session:
        try:
            new_customer = UserORM(
                first_name=userdata.first_name,
                last_name=userdata.last_name,
                email=userdata.email,
                password_hash=AuthManagement.hash_password(userdata.password)
            )
            session.add(new_customer)
            await session.commit()
            await session.refresh(new_customer)

            return ApiResponse(status_code=200,
                               message='Success',
                               detail={
                "message": f"User has been created successfully {new_customer.id}",
            })
        # need to add specific noreply to send otp
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user already exists with the provided email"
            )


async def check_user_creds(creds_data: LoginUser):
  async with async_session_factory() as session:
    query = select(UserORM).where(UserORM.email == creds_data.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not AuthManagement.password_checker(hashed_password=user.password_hash, 
                      password=creds_data.password):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
      )

    token = AuthManagement.encode_jwt({"user_id": user.id}, exp=300)

    return token


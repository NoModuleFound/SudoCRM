from typing import Annotated
from fastapi import APIRouter, Depends, Body
from backend.api.schemas.users_schema import CreateUser, LoginUser
from backend.shared.db.quaries.services.user_service import create_new_user, check_user_creds

router = APIRouter(prefix='/users',tags=['User Management'])


@router.post('/create-user')
async def create_user(user_data: Annotated[CreateUser, Body()]):
  return await create_new_user(user_data)



@router.post('/login-user')
async def check_login_user(userdata: Annotated[LoginUser, Body()]):
  return await check_user_creds(userdata)
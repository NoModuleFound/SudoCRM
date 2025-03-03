from .utils import BaseModel
from enum import Enum
from pydantic import EmailStr, field_validator

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr



class RoleUser(str, Enum):
  superuser = 'superuser'
  admin = 'admin'
  worker = 'worker'
  not_identified = 'user'


# ------------------------- User DTO ------------------------- #
class UserBaseDTO(BaseModel):

    first_name: str
    last_name: Optional[str] = None
    role: RoleUser

class UserCreateDTO(UserBaseDTO):
    password: str
    phone_number: int

class UserUpdateDTO(BaseModel):
    
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None

class UserReadDTO(UserBaseDTO):
    
    
    id: int

    @field_validator('role', mode='before')
    @classmethod
    def validate_role(cls, v):
        if isinstance(v, str):
            return RoleUser(v)
        return v

# ------------------------- Credential DTO ------------------------- #
class CredentialBaseDTO(BaseModel):
    
    
    email: Optional[EmailStr] = None
    phone_number: int
    user_id: int

class CredentialCreateDTO(CredentialBaseDTO):
    password: str  # Used for user registration

class CredentialReadDTO(CredentialBaseDTO):
    id: int



# ------------------------- Telegram Data DTO ------------------------- #
class TelegramDataBaseDTO(BaseModel):
    
    
    telegram_id: int
    telegram_username: Optional[str] = None
    user_id: int

class TelegramDataReadDTO(TelegramDataBaseDTO):
    id: int

    


# ------------------------- Organization DTO ------------------------- #
class OrganizationBaseDTO(BaseModel):
    
    
    name: str
    phone_number: Optional[str] = None
    user_id: int

class OrganizationCreateDTO(OrganizationBaseDTO):
    pass  # No extra fields needed

class OrganizationReadDTO(OrganizationBaseDTO):
    id: int
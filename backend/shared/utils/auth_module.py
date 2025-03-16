import jwt
import bcrypt
from pathlib import Path
from config import settings
from datetime import datetime


class AuthManagement():
  def encode_jwt(payload, exp: int) -> str:
      try:
          payload.update({"exp": datetime.now().timestamp() + exp})
          encoded = jwt.encode(payload, key=(Path(settings.PRIVATE_KEY)).read_text(), algorithm=settings.ALGORITHM)
          return encoded
      except Exception as e:
          raise ValueError(f"Error encoding JWT: {e}")


  def decode_jwt(token: str) -> dict:
      try:
          decoded = jwt.decode(token, key=(Path(settings.PUBLIC_KEY).read_text()), 
                              algorithms=[settings.ALGORITHM])
          return decoded

      except Exception as e:
          raise ValueError(f"Error decoding JWT: {e}")


  def hash_password(password: str) -> bytes:
      try:
          pwd_bytes = password.encode('utf-8')
          salt = bcrypt.gensalt()
          hashed_password = bcrypt.hashpw(password=pwd_bytes, 
                                          salt=salt)
          return hashed_password
      except Exception as e:
          raise ValueError(f"Error hashing password: {e}")


  def password_checker(hashed_password: bytes, 
                          password: str) -> bool:
      try:
          return bcrypt.checkpw(password.encode('utf-8'), 
                                hashed_password)
      except Exception as e:
          raise ValueError(f"Error validating password: {e}")
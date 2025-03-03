from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=True
  )

  SECRET_KEY: str
  PRIVATE_KEY: str
  PUBLIC_KEY: str
  ALGORITHM: str


  @property
  def DATABASE_URL(self) -> str:
    return "sqlite+aiosqlite:///backend/shared/db.sqlite"


settings = Settings()
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLAlchemyEnum, Index, UniqueConstraint, Table
from backend.api.schema.user_schma import RoleUser
from datetime import datetime


class UserORM(SQLModel, table=True):
    """User model representing system users with role-based access control"""
    __tablename__ = "users"

    # Indexes and constraints
    __table_args__ = (
        Index("idx_user_role", "role"),  # Index for role-based queries
        Index("idx_user_search", "first_name", "last_name"),  # Composite index for name searches
        UniqueConstraint("username", name="uq_username"),
        {"extend_existing": True}
    )

    # Primary fields
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False, max_length=50)
    last_name: Optional[str] = Field(nullable=True, max_length=50)
    username: Optional[str] = Field(nullable=True, max_length=50)
    
    # Role and status
    role: RoleUser = Field(
        sa_column=Column(
            SQLAlchemyEnum(RoleUser),
            default=RoleUser.not_identified,
            nullable=False  # Changed to non-nullable
        )
    )
    is_active: bool = Field(default=True, nullable=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships with cascade delete
    credentials: Optional["CredentialORM"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all, delete-orphan"
        }
    )
    telegram_data: Optional["TelegramDataORM"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all, delete-orphan"
        }
    )
    organizations: List["OrganizationORM"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class CredentialORM(SQLModel, table=True):
    """Credentials for user authentication"""
    __tablename__ = "credentials"

    __table_args__ = (
        Index("idx_credentials_email", "email"),
        Index("idx_credentials_phone", "phone_number"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str] = Field(nullable=True, unique=True, max_length=255)
    phone_number: str = Field(nullable=False, unique=True, max_length=20)
    password_hash: bytes = Field(nullable=False)
    last_login: Optional[datetime] = Field(nullable=True)
    
    # Foreign key with cascade delete
    user_id: int = Field(foreign_key="users.id", nullable=False, unique=True)
    user: "UserORM" = Relationship(back_populates="credentials")


class TelegramDataORM(SQLModel, table=True):
    """Telegram-specific user data"""
    __tablename__ = "telegram_data"
    
    __table_args__ = (
        Index("idx_telegram_id", "telegram_id"),
        Index("idx_telegram_username", "telegram_username"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(nullable=False, unique=True)
    telegram_username: Optional[str] = Field(nullable=True, max_length=32)
    is_active: bool = Field(default=True, nullable=False)
    last_interaction: Optional[datetime] = Field(nullable=True)
    
    # Foreign key with cascade delete
    user_id: int = Field(foreign_key="users.id", nullable=False, unique=True)
    user: "UserORM" = Relationship(back_populates="telegram_data")


class OrganizationORM(SQLModel, table=True):
    """Organization information"""
    __tablename__ = "organizations"
    
    __table_args__ = (
        Index("idx_org_name", "name"),
        Index("idx_org_status", "status"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, max_length=100)
    phone_number: Optional[str] = Field(nullable=True, max_length=20)
    status: str = Field(default="active", nullable=False)  # active, inactive, suspended
    description: Optional[str] = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    # Foreign key with cascade delete
    user_id: int = Field(foreign_key="users.id", nullable=False)
    user: "UserORM" = Relationship(back_populates="organizations")
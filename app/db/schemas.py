from datetime import datetime

from pydantic import BaseModel, Field, field_validator


MAX_BCRYPT_PASSWORD_BYTES = 72


def validate_bcrypt_password(value: str) -> str:
    if len(value.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError("Password cannot be longer than 72 bytes")
    return value


# Schemas for Note
class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
    
    
# Schemas for User
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_bcrypt_password(value)
    
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    model_config = {
        "from_attributes": True
    }


class AdminUserResponse(UserResponse):
    created_at: datetime
    note_count: int = 0


class AdminUserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = Field(default=None, min_length=1, max_length=100)
    is_admin: bool | None = None
    
    
class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_bcrypt_password(value)
    
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

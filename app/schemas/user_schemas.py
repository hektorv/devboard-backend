from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime
from typing import List
from pydantic import ConfigDict


class UserCreate(BaseModel):
    display_name: str = Field(..., max_length=255)
    email: EmailStr


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr]


class UserOut(BaseModel):
    id: int
    display_name: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    data: UserOut
    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    data: List[UserOut]
    paging: dict
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Annotated, Optional
from datetime import datetime
from enum import Enum

PyObjectID = Annotated[str, BeforeValidator(str)]

class Gender(str, Enum):
    male = "male"
    female = "female"

class Profile(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    age: int = Field(...)
    salary: float = Field(...)
    gender: Gender

class User(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    profile: Profile = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)   

class UserOutput(User):
    id: PyObjectID = Field(alias="_id", default=None)
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    profile: Optional[Profile] = None
    created_at: Optional[datetime] =None
    updated_at: Optional[datetime] = None   

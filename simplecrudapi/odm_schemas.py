from pydantic import Field, BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from beanie import Document

class Profile(Document):
    id: Optional[str] = Field(alias="_id")
    username: str 
    name: str 
    address: str
    mail: str

    class Settings:
        name = "profiles"

    class Config:
        populate_by_name = True
class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    mail: Optional[str] = None
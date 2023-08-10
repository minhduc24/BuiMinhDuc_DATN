from pydantic import BaseModel
from typing import List, Optional

class UserSchemas(BaseModel):
    name: Optional[str]
    password: Optional[str]
    image: Optional[str]
    email: Optional[str]
    class Config:
        orm_mode = True

class UploadData(BaseModel):
    userId: int
    class Config:
        orm_mode = True
class UserEmail(BaseModel):
    email: str

class UserUpdate(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    class Config:
        orm_mode = True
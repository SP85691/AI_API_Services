# Create the schema for User, chatPrompts and chatResponses
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class RegisterUser(BaseModel):
    name: str
    username: str = Field(min_length=5, max_length=15)
    email: EmailStr
    password: str = Field(min_length=8)
    isActive: Optional[bool] = True
    isAdmin: Optional[bool] = True

class LoginUser(BaseModel):
    username: str = Field(min_length=5, max_length=15)
    password: str = Field(min_length=8)
    

class CurrentUser(BaseModel):
    name : str
    username : str
    email : str
    isAdmin : bool

class User(BaseModel):
    id: Optional[int] = None
    name: str 
    username: str = Field(min_length=5, max_length=15)
    email: EmailStr
    password: str = Field(min_length=8)
    isActive: Optional[bool] = True
    isAdmin: Optional[bool] = True
    age: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    registered: bool = True
    about: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    
    class Config:
        orm_mode = True

        
class chatPrompts(BaseModel):
    id: int
    user_id: int
    prompt: str
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    
    class Config:
        orm_mode = True
        
class chatResponses(BaseModel):
    id: int
    user_id: int
    prompt: str
    response: str
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    
    class Config:
        orm_mode = True
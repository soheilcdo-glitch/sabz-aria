from pydantic import BaseModel, Field
from typing import Optional
import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    national_id: Optional[str] = Field(None, regex=r'^\d{10}$')
    card_number: Optional[str] = Field(None, regex=r'^[\d-]{0,19}$')
    phone: Optional[str] = Field(None, regex=r'^\d{0,11}$')
    birth_date: Optional[datetime.date]
    role: Optional[str] = "کارمند"

class UserOut(BaseModel):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    national_id: Optional[str]
    card_number: Optional[str]
    phone: Optional[str]
    birth_date: Optional[datetime.date]
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime]
    role: str
    is_active: bool
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    national_id: Optional[str] = Field(None, regex=r'^\d{10}$')
    card_number: Optional[str] = Field(None, regex=r'^[\d-]{0,19}$')
    phone: Optional[str] = Field(None, regex=r'^\d{0,11}$')
    birth_date: Optional[datetime.date]
    role: Optional[str]
    is_active: Optional[bool]

class ChangePassword(BaseModel):
    old_password: Optional[str]
    new_password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginHistoryOut(BaseModel):
    id: int
    user_id: int
    username: str
    timestamp: datetime.datetime
    ip: Optional[str]
    class Config:
        orm_mode = True

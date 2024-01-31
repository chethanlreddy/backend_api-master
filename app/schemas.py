import string
from unicodedata import numeric
from click import option
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer


class userCreate(BaseModel):
    email: EmailStr
    password: str
    # phone_number: str


class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class tokenData(BaseModel):
    id: Optional[str] = None


class tokenOut(BaseModel):
    access_token: str
    token_type: str


class userCollect(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    # phone_number: str


class userCollectOut(userCollect):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class user_location_data_in(BaseModel):
    digital_access_code: str
    Aadhaar : str
    address: str


class user_location_data_out(user_location_data_in):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class location_data_in(BaseModel):
    latitude: str
    longitude: str


class location_data_out(location_data_in):
    digital_access_code: str
    created_at: datetime

    class Config:
        orm_mode = True


class user_data_out(userOut):
    user_data: userCollectOut
    user_location_data: user_location_data_out

    class Config:
        orm_mode = True


class new_password_in(BaseModel):
    password: str
    retype_password: str

    class Config:
        orm_mode = True

class phone_number_in(BaseModel):
    phone_number: str

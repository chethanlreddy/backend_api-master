from cgi import print_arguments
import string
from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Numeric, BigInteger
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    # phone_number = Column(Numeric, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_data = relationship('User_data', uselist=False)
    user_location_data = relationship('User_location_data', uselist=False)


class User_data(Base):
    __tablename__ = 'users_data'
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    # phone_number = Column(Numeric, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class User_location_data(Base):
    __tablename__ = 'users_location_data'
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    digital_access_code = Column(String(length=30), ForeignKey(
        'digital_access_code_location.digital_access_code', ondelete='CASCADE'), nullable=False)
    address = Column(String, nullable=False)
    Aadhaar = Column(String(length=20), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Digital_access_code_location(Base):
    __tablename__ = 'digital_access_code_location'
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    digital_access_code = Column(
        String(length=20), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

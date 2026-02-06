from sqlalchemy import (
    create_engine, Column, Integer, String, SmallInteger, ForeignKey, DateTime
)
from sqlalchemy.orm import declarative_base, relationship, Session

from Models.Base import Base

"""
  id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Para el hash de bcrypt
    name VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    birth_date DATE
"""

class User(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key = True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    lastname = Column(String)
    email = Column(String)
    phone = Column(String)
    birth_date = Column(DateTime)
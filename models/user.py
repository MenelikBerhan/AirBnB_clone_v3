#!/usr/bin/python3
""" holds class User"""
import models
from hashlib import md5
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Blueprint of the User Class"""
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade='all, delete-orphan')
        reviews = relationship("Review", backref="user",
                               cascade='all, delete-orphan')
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Setter and getter of password attribute"""
        return self._password

    @password.setter
    def password(self, pss):
        self._password = md5(pss.encode()).hexdigest()

import datetime
from config import Config
from Models.Base import Base
from Models.Users import User

import pymongo


from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import Session


class UsersRepository():
    
    _instancia = None
    nomber = ""

    def __new__(cls):

        if cls._instancia is None:
            # Crea la instancia única
            cls._instancia = super(UsersRepository, cls).__new__(cls)

            if(Config.USE_MONGO):
                
                myclient = pymongo.MongoClient(Config.MONGODB_URI)
                cls._instancia.engine = myclient[Config.MONGO_DB_NAME]

            else:

                cls._instancia.engine = create_engine(
                    Config.SQL_URL,
                    echo=False
                )

                Base.metadata.create_all(cls._instancia.engine) 

        return cls._instancia


    def getUserByUsername(self, username):

        if(Config.USE_MONGO):

            return self.engine.find_one({"username": username})

        else:

            with Session(self.engine) as session:

                return session.query(User).filter_by(username=username).all()

   
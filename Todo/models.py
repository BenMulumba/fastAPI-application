from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey

#create data base for users
class Users (Base):
    __tablename__ = 'Users'

    id=Column (Integer,primary_key=True, index=True)
    email = Column (String, unique=True)
    username = Column (String, unique= True)
    first_name = Column(String) 
    last_name = Column(String)
    hashed_password = Column (String)
    is_active = Column (Boolean, default= True)
    role = Column (String)

class todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer,primary_key=True, index=True)
    title = Column (String)
    description = Column (String)
    priority = Column (String)
    complete = Column (Boolean, default= False)
    owner_id = Column (Integer, ForeignKey (Users.id))

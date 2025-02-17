from sqlalchemy import Column, String, Integer
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
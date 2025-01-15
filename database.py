import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:password@localhost/test"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

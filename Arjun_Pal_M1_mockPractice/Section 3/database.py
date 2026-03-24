from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./university.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base() # this is your PARENT class for all database models convert it in ORM
# # this function is returning a special class.
# if you remove Base class, sqlalchemy will not treat the child class as a table
# 1. Register the child class as a table
# 2. Store metadata
# 3. Connect class variables and functions to the database engine

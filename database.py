from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv() #Loads .env variables
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) #creates the SQLAlchemy engine
SessionLocal = sessionmaker(bind = engine, autoflush=False) #SessionLocal is a session factory.
Base = declarative_base() #creates the base class for your database models.


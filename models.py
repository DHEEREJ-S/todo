from sqlalchemy import Column, Integer, String, Boolean
from database import Base;

class Todo(Base):  #SQLAlchemy will understand that this class represents a database table
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    
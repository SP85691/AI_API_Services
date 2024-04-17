from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.db_setup import Base

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
  name = Column(String, nullable=False)
  username = Column(String, nullable=False, unique=True)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  isActive = Column(Boolean, default=True, nullable=True)
  isAdmin = Column(Boolean, default=False, nullable=True)
  age = Column(Integer, nullable=True)
  address = Column(String, nullable=True)
  phone = Column(String, nullable=True)
  gender = Column(String, nullable=True)
  registered = Column(Boolean, default=True, nullable=True)
  about = Column(String, nullable=True)
  title = Column(String, nullable=True)
  body = Column(String, nullable=True)
  createdAt = Column(DateTime, default=func.now())
  updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
  chats = relationship("chatPrompts", back_populates="user")
  responses = relationship("chatResponses", back_populates="user")


class chatPrompts(Base):
  __tablename__ = "chat_prompts"
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  prompt = Column(String)
  createdAt = Column(DateTime, default=func.now())
  updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

  user = relationship("User", back_populates="chats")


class chatResponses(Base):
  __tablename__ = "chat_responses"
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  prompt = Column(String)
  response = Column(String)
  createdAt = Column(DateTime, default=func.now())
  updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

  user = relationship("User", back_populates="responses")
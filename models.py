from sqlalchemy import Column, Integer, String
from database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    message = Column(String)

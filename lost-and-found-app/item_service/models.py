from sqlalchemy import Column, Integer, String, Date, DateTime
from database import Base
from datetime import datetime, timezone


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    type = Column(String, default="lost") 
    reported_by = Column(String)
    image = Column(String, nullable=True) 


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)  
    content = Column(String)
    commenter = Column(String)
    time = Column(DateTime, default=lambda: datetime.now(timezone.utc)) 


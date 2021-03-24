from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Text, ForeignKeyConstraint, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'
    id1 = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    date = Column(Date, nullable=False)


class Info(Base):
    __tablename__ = 'info'
    team1 = Column(String(20), primary_key=True)
    team2 = Column(String(20), nullable=False)
    id2 = Column(Integer, ForeignKey('events.id1'), nullable=False)
    id = relationship('Event', foreign_keys=[id2])

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String,Integer,Float,DateTime

Base = declarative_base()

class DJI(Base):
    __tablename__ = 'DJI'.lower()
    index = Column(Integer())
    date = Column(DateTime(timezone = False), primary_key = True)
    open = Column(Float())
    high = Column(Float())
    low = Column(Float())
    close = Column(Float())
    adjclose = Column(Float())
    volume = Column(Float())
class IXIC(Base):
    __tablename__ = 'ixic'.lower()
    index = Column(Integer())
    date = Column(DateTime(timezone = False), primary_key = True)
    open = Column(Float())
    high = Column(Float())
    low = Column(Float())
    close = Column(Float())
    adjclose = Column(Float())
    volume = Column(Float())
class GSPC(Base):
    __tablename__ = 'gspc'.lower()
    index = Column(Integer())
    date = Column(DateTime(timezone = False), primary_key = True)
    open = Column(Float())
    high = Column(Float())
    low = Column(Float())
    close = Column(Float())
    adjclose = Column(Float())
    volume = Column(Float())
class CRUDE_OIL(Base):
    __tablename__ = 'CRUDE_OIL'.lower()
    index = Column(Integer())
    date = Column(DateTime(timezone = False), primary_key = True)
    open = Column(Float())
    high = Column(Float())
    low = Column(Float())
    close = Column(Float())
    adjclose = Column(Float())
    volume = Column(Float())

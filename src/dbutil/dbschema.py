from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint

Base = declarative_base()

class BrentOptionData(Base):
    __tablename__ = 'BrentOptionData'
    DateAsOf = Column(Integer)
    FutureExpiryDate = Column(Integer)
    OptionType = Column(String(10))
    StrikePrice = Column(Float)
    CurrentPrice = Column(Float)
    ImpliedVol = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('DateAsOf', 'FutureExpiryDate', 'OptionType', 'StrikePrice'), {})


def get_optiondata_dbschmea():
    return Base
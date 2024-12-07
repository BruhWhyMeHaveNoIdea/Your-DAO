from bot.db.db import Base
from sqlalchemy import Column, Integer, BigInteger, String


class Banned(Base):
    __tablename__ = 'banned'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_nickname = Column(String)

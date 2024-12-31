from bot.db.db import Base
from sqlalchemy import Column, Integer, BigInteger, String


class Admins(Base):
    __tablename__ = 'admin'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_nickname = Column(String)

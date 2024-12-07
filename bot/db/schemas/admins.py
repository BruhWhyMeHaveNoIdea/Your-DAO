from bot.db.db import Base
from sqlalchemy import Column, Integer, BigInteger, String


class Admins(Base):
    __tablename__ = 'admin'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_nickname = Column(String)

    def __repr__(self):
        return f"ADMIN\tID: {self.id}\n{' ' * 5}\tUSER_ID: {self.user_id}\n"

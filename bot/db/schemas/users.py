from xmlrpc.client import DateTime


from bot.db.db import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime, BigInteger


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger)
    subscription_type = Column(Integer)  # 0, 1, 2; без подписки; без жпт; с жпт
    referral_users = Column(Integer)
    bonuses = Column(Integer)
    sub_days = Column(Integer)
    active = Column(Boolean)
    registration_date = Column(DateTime(timezone=True))

    def __repr__(self):
        text = f"USER\tID: {self.id}\n"
        rows = {
            "USER_ID": self.user_id,
            "SUBSCRIPTION_TYPE": self.subscription_type,
            "REFERRAL_USERS": self.referral_users,
            "BONUSES": self.bonuses,
            "SUB_DAYS": self.sub_days,
            "ACTIVE": self.active,
        }
        for k, v in rows.items():
            text += f"\t{k}: {v}\n"

        # return f"""USER\tID: {self.id}\n{' ' * 4}\tUSER_ID: {self.user_id}"""
        return text

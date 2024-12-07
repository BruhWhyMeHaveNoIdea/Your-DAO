from datetime import datetime

from pydantic import BaseModel


class Users(BaseModel):
    user_id: int
    subscription_type: int
    referral_users: int
    bonuses: int
    sub_days: int
    active: bool
    registration_date: datetime


"""user_id = Column(Integer)
    subscription_type = Column(Integer)  # 0, 1, 2; без подписки; без жпт; с жпт
    referral_users = Column(Integer)
    bonuses = Column(Integer)
    sub_days = Column(Integer)
"""

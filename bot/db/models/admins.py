from pydantic import BaseModel


class Admins(BaseModel):
    user_nickname: str

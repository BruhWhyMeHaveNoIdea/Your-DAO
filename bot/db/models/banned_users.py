from pydantic import BaseModel


class Banned(BaseModel):
    user_nickname: str
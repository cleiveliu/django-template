from core.shortcuts import BaseModel


class SchemaLogin(BaseModel):
    username: str
    password: str

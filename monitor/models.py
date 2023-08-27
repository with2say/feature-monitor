# monitor/models.py

from pydantic import BaseModel


class NodeInfo(BaseModel):
    name: str
    hostname: str
    port: int
    username: str
    password: str

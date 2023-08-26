# monitor/models.py

from pydantic import BaseModel

class NodeInfo(BaseModel):
    name: str
    address: str
    username: str
    password: str

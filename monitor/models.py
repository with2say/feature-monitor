# monitor/models.py

from pydantic import BaseModel


class NodeInfo(BaseModel):
    name: str
    hostname: str
    port: int


class NodeName(BaseModel):
    name: str


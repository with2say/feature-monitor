# monitor/api/routers.py

from fastapi import APIRouter
from monitor.core.monitoring import (add_node as add_node_api,
                                     delete_node as delete_node_api)
from monitor.models import NodeInfo

router = APIRouter()


@router.post("/add_node")
def add_node(node_info: NodeInfo = NodeInfo(name='node01', hostname="172.28.201.169", port=10001)):
    add_node_api(node_info)
    return {"status": "success"}


@router.post("/delete_node")
def delete_node(node_name: str = 'node01'):
    delete_node_api(node_name)
    return {"status": "success"}




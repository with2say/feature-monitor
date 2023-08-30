from fastapi import APIRouter
from monitor.api.api import (add_node_api, delete_node_api)
from monitor.models import NodeInfo, NodeName

router = APIRouter()


@router.post("/add_node")
def add_node(node_info: NodeInfo = NodeInfo(name='node01', hostname="172.28.201.169", port=10001)):
    add_node_api(node_info)
    return {"status": "success"}


@router.post("/delete_node")
def delete_node(node_name: NodeName = NodeName(name='node_test')):
    delete_node_api(node_name)
    return {"status": "success"}


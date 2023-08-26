# monitor/api/routers.py

from fastapi import APIRouter
from ..core.monitoring import ExecutionManager
from ..models import NodeInfo

router = APIRouter()

@router.post("/add_node")
def add_node(node_info: NodeInfo):
    # 노드 추가 로직
    return {"status": "success"}

@router.post("/modify_node")
def modify_node(node_info: NodeInfo):
    # 노드 변경 로직
    return {"status": "success"}

@router.post("/delete_node")
def delete_node(node_info: NodeInfo):
    # 노드 삭제 로직
    return {"status": "success"}

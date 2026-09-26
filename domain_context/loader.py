"""读取并检查共享领域资料。"""

import json
from pathlib import Path

REQUIRED = {"domain", "version", "sample_id", "record_types", "workflow_states", "facts", "sample"}

# 需求强约束：缺少这些记录类型或流程状态，领域资料就不足以支撑
# 窗口化统计、领域归一、名单重现与作者申诉，视为不完整。
REQUIRED_RECORD_TYPES = {"统计窗口", "领域基准", "数据快照", "申诉记录"}
REQUIRED_STATES = {"观察中", "待复核", "申诉中"}

def load_domain(path: Path) -> dict:
    """返回字段完整且具有流程状态的领域资料。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not REQUIRED.issubset(value):
        raise ValueError("领域资料缺少必要字段")
    if value["version"] < 1 or len(value["record_types"]) < 3 or len(value["workflow_states"]) < 3:
        raise ValueError("领域资料内容不完整")
    if not REQUIRED_RECORD_TYPES.issubset(value["record_types"]):
        raise ValueError("领域资料缺少关键记录类型")
    if not REQUIRED_STATES.issubset(value["workflow_states"]):
        raise ValueError("领域资料缺少关键流程状态")
    return value

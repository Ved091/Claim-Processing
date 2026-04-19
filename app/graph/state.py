from typing import Dict, List, Any
from pydantic import BaseModel

class GraphState(BaseModel):
    claim_id: str
    pages: List[str]
    document_map: Dict[int, str] = {}
    id_data: Dict[str, Any] = {}
    discharge_data: Dict[str, Any] = {}
    bill_data: Dict[str, Any] = {}
    final_output: Dict[str, Any] = {}
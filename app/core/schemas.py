from pydantic import BaseModel
from typing import Dict, Any

class ProcessResponse(BaseModel):
    claim_id: str
    document_map: Dict[str, str]
    extracted_data: Dict[str, Any]
    status: str
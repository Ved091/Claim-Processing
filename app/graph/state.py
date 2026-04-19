from typing import Dict, List, Any, Annotated
from typing_extensions import TypedDict

def merge_dicts(left: dict, right: dict) -> dict:
    """Merge two dictionaries, with right overriding left."""
    return {**left, **right}

class GraphState(TypedDict):
    claim_id: str
    pages: List[str]
    document_map: Annotated[Dict[int, str], merge_dicts]
    id_data: Annotated[Dict[str, Any], merge_dicts]
    discharge_data: Annotated[Dict[str, Any], merge_dicts]
    bill_data: Annotated[Dict[str, Any], merge_dicts]
    final_output: Annotated[Dict[str, Any], merge_dicts]
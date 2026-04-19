def aggregate(state):
    return {
        "final_output": {
            "claim_id": state["claim_id"],
            "document_map": state["document_map"],
            "extracted_data": {
                "identity": state["id_data"],
                "discharge_summary": state["discharge_data"],
                "itemized_bill": state["bill_data"]
            },
            "status": "success"
        }
    }
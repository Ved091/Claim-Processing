from app.graph.workflow import run_workflow

def test_empty_pages():
    result = run_workflow("test_claim", [])

    assert result["claim_id"] == "test_claim"
    assert result["status"] == "success"
    assert "extracted_data" in result
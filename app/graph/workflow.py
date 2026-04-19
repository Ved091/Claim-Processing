from langgraph.graph import StateGraph, END
from app.graph.state import GraphState

from app.services.segregator import segregate_pages
from app.agents.id_agent import extract_id_data
from app.agents.discharge_summary_agent import extract_discharge_data
from app.agents.itemized_bill_agent import extract_bill_data


def segregator_node(state: GraphState):
    return {"document_map": segregate_pages(state["pages"])}


def id_node(state: GraphState):
    pages = [
        state["pages"][i]
        for i, t in state["document_map"].items()
        if t == "identity_document"
    ]
    return {"id_data": extract_id_data(pages)}


def discharge_node(state: GraphState):
    pages = [
        state["pages"][i]
        for i, t in state["document_map"].items()
        if t == "discharge_summary"
    ]
    return {"discharge_data": extract_discharge_data(pages)}


def bill_node(state: GraphState):
    pages = [
        state["pages"][i]
        for i, t in state["document_map"].items()
        if t == "itemized_bill"
    ]
    return {"bill_data": extract_bill_data(pages)}


def aggregator_node(state: GraphState):
    return {
        "final_output": {
            "claim_id": state["claim_id"],
            "document_map": state["document_map"],
            "extracted_data": {
                "identity": state.get("id_data", {}),
                "discharge_summary": state.get("discharge_data", {}),
                "itemized_bill": state.get("bill_data", {})
            },
            "status": "success"
        }
    }


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("segregator", segregator_node)
    builder.add_node("id_agent", id_node)
    builder.add_node("discharge_agent", discharge_node)
    builder.add_node("bill_agent", bill_node)
    builder.add_node("aggregator", aggregator_node)

    builder.set_entry_point("segregator")

    builder.add_edge("segregator", "id_agent")
    builder.add_edge("segregator", "discharge_agent")
    builder.add_edge("segregator", "bill_agent")

    builder.add_edge("id_agent", "aggregator")
    builder.add_edge("discharge_agent", "aggregator")
    builder.add_edge("bill_agent", "aggregator")

    builder.add_edge("aggregator", END)

    return builder.compile()


graph = build_graph()


def run_workflow(claim_id, pages):
    state = {
        "claim_id": claim_id,
        "pages": pages,
        "document_map": {},
        "id_data": {},
        "discharge_data": {},
        "bill_data": {},
        "final_output": {}
    }

    result = graph.invoke(state)

    return result["final_output"]
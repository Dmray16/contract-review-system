from langgraph.graph import StateGraph, START, END
import json


def agent1_chunker(state):

    contract = state["contract"]

    chunks = contract.split("\n\n")

    return {
    **state,
    "chunks": chunks
}

def agent2_compliance(state):

    chunks = state["chunks"]

    results = []

    for chunk in chunks:

        if "deliver" in chunk.lower():
            result = "Delivery obligation identified."

        elif "pay" in chunk.lower():
            result = "Payment obligation identified."

        elif "terminate" in chunk.lower():
            result = "Termination condition identified."

        else:
            result = "No specific compliance requirement identified."

        results.append(result)

    return {
    **state,
    "compliance": results
   }   
def agent3_risk(state):

    chunks = state["chunks"]
    compliance_results = state["compliance"]

    report = []

    for i in range(len(chunks)):

        compliance = compliance_results[i]

        if "termination" in compliance.lower():
            risk = "High"

        elif "payment" in compliance.lower():
            risk = "Medium"

        elif "delivery" in compliance.lower():
            risk = "Medium"

        else:
            risk = "Low"

        report.append({
            "chunk": i + 1,
            "contract_clause": chunks[i].strip(),
            "compliance": compliance,
            "risk": risk
        })

    risks = [item["risk"] for item in report]

    if "High" in risks:
        overall_risk = "High"
    elif "Medium" in risks:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"

    return {
        **state,
        "report": report,
        "overall_risk": overall_risk
    }
builder = StateGraph(dict)

builder.add_node("agent1", agent1_chunker)
builder.add_node("agent2", agent2_compliance)
builder.add_node("agent3", agent3_risk)

builder.add_edge(START, "agent1")
builder.add_edge("agent1", "agent2")
builder.add_edge("agent2", "agent3")
builder.add_edge("agent3", END)

graph = builder.compile()

result = graph.invoke({
    "contract": """
Delivery:
The vendor must deliver 500 units every month.

Payment:
The buyer must pay invoices within 30 days.

Termination:
Either party may terminate for material breach.
"""
})

import json

print(json.dumps({
    "overall_risk": result["overall_risk"],
    "findings": result["report"]
}, indent=2))
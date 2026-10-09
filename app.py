import streamlit as st
from langgraph.graph import StateGraph, START, END

# Agent 1: Split the contract into chunks
def agent1_chunker(state):
    contract = state["contract"]
    chunks = contract.split("\n\n")

    return {
        **state,
        "chunks": chunks
    }


# Agent 2: Identify compliance obligations
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


# Agent 3: Evaluate risk and compile the report
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


# Build the LangGraph workflow
builder = StateGraph(dict)

builder.add_node("agent1", agent1_chunker)
builder.add_node("agent2", agent2_compliance)
builder.add_node("agent3", agent3_risk)

builder.add_edge(START, "agent1")
builder.add_edge("agent1", "agent2")
builder.add_edge("agent2", "agent3")
builder.add_edge("agent3", END)

graph = builder.compile()


# Streamlit user interface
st.title("Contract Review System")

contract = st.text_area(
    "Enter your contract:",
    height=300
)

if st.button("Analyze Contract"):
    if contract.strip():
        result = graph.invoke({
            "contract": contract
        })

        st.session_state["report"] = result
    else:
        st.warning("Please enter a contract first.")


# Display the saved report
if "report" in st.session_state:
    saved_report = st.session_state["report"]

    st.subheader("Overall Risk")
    st.write(saved_report["overall_risk"])

    st.subheader("Contract Findings")

    for finding in saved_report["report"]:
        st.write(f"**Clause {finding['chunk']}**")
        st.write(finding["contract_clause"])
        st.write(f"Compliance: {finding['compliance']}")
        st.write(f"Risk: {finding['risk']}")

    with st.expander("View Full JSON Report"):
        st.json(saved_report)
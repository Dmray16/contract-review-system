from agent1 import chunk_document
from agent2 import check_compliance
from agent3 import evaluate_risk
import json


contract = """
Delivery:
The vendor must deliver 500 units every month.

Payment:
The buyer must pay invoices within 30 days.

Termination:
Either party may terminate for material breach.
"""


# Agent 1: chunk the contract
chunks = chunk_document(contract)


# Agent 2: check each chunk
report = []

for i, chunk in enumerate(chunks):

    compliance = check_compliance(chunk)
    risk = evaluate_risk(compliance)

    report.append({
        "chunk": i + 1,
        "content": chunk,
        "compliance": compliance,
        "risk": risk.replace("Risk: ", "")
    })


print("\nFINAL REPORT")
print(json.dumps(report, indent=2))

# Agent 3: evaluate risk for each compliance result
risk = evaluate_risk(compliance)
print(risk)
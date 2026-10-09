def evaluate_risk(compliance_result):

    if "termination" in compliance_result.lower():
        return "Risk: High"

    elif "payment" in compliance_result.lower():
        return "Risk: Medium"

    elif "delivery" in compliance_result.lower():
        return "Risk: Medium"

    else:
        return "Risk: Low"


compliance_results = [
    "Delivery obligation identified.",
    "Payment obligation identified.",
    "Termination condition identified."
]

for i, result in enumerate(compliance_results):

    risk = evaluate_risk(result)

    print(f"\nChunk {i + 1}:")
    print(result)
    print(risk)
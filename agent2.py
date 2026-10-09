def check_compliance(chunk):

    if "deliver" in chunk.lower():
        return "Delivery obligation identified."

    elif "pay" in chunk.lower():
        return "Payment obligation identified."

    elif "terminate" in chunk.lower():
        return "Termination condition identified."

    else:
        return "No specific compliance requirement identified."


chunks = [
    "Delivery:\nThe vendor must deliver 500 units every month.",
    "Payment:\nThe buyer must pay invoices within 30 days.",
    "Termination:\nEither party may terminate for material breach."
]

for i, chunk in enumerate(chunks):

    result = check_compliance(chunk)

    print(f"\nChunk {i + 1}:")
    print(result)
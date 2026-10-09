def chunk_document(text):

    chunks = text.split("\n\n")

    return chunks
contract = """
Delivery:
The vendor must deliver 500 units every month.

Payment:
The buyer must pay invoices within 30 days.

Termination:
Either party may terminate for material breach.
"""

chunks = chunk_document(contract)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)
import os
import json
import chromadb
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# ChromaDB setup

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="contract_chunks"
)

chroma_client.delete_collection(name="contract_chunks")

collection = chroma_client.get_or_create_collection(
    name="contract_chunks"
)



# Hugging Face setup

load_dotenv()

token = os.getenv("HF_TOKEN")

client = InferenceClient(
    provider="auto",
    api_key=token
)



# Load knowledge base

knowledge_base = []

for filename in os.listdir("knowledge_base"):
    if filename.endswith(".txt"):
        path = os.path.join("knowledge_base", filename)

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        knowledge_base.append({
            "filename": filename,
            "content": content
        })


print("\nKnowledge base loaded:")


for document in knowledge_base:
    print("-", document["filename"])

# Simple document chunking

def chunk_text(text):
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    return paragraphs

# Add documents to ChromaDB

for document in knowledge_base:
    chunks = chunk_text(document["content"])

    for i, chunk in enumerate(chunks):
        collection.add(
    documents=[f"Document: {document['filename']}\n\n{chunk}"],
    ids=[f"{document['filename']}_{i}"]
)

print("\nDocuments added to ChromaDB:")
print(collection.count())



# Get contract from user

contract = input("\nEnter a vendor contract clause: ")




# Retrieve relevant documents

search_results = collection.query(
    query_texts=[contract],
    n_results=2
)

relevant_content = search_results["documents"][0]
relevant_ids = search_results["ids"][0]

print("\nRelevant chunks retrieved:")

evidence = []

for chunk_id, content in zip(relevant_ids, relevant_content):
    print("\nChunk ID:", chunk_id)
    print(content)

    evidence.append(
        f"[Historical Evidence - {chunk_id}]\n{content}"
    )

relevant_content = "\n\n".join(evidence)



# Send contract to LLM

prompt = f"""
You are a contract compliance assistant.

Analyze the following vendor contract clause:

{contract}

Here is relevant information retrieved from previous contracts:

{relevant_content}

Use the retrieved information as historical evidence only.

IMPORTANT RULES:
1. Treat the current contract as the primary source of truth.
2. Do not treat terms from previous contracts as requirements of the current contract.
3. A difference between the current contract and a previous contract is NOT automatically a risk.
4. Use previous contracts only to identify relevant precedents, lessons, or potential risks.
5. Do not invent obligations, deadlines, or risks that are not supported by the current contract.
6. Base the final risk primarily on the current contract.
7. Do not describe a difference from a historical contract as a risk unless the current contract itself provides evidence that the difference creates a compliance, operational, financial, or legal problem.
8. Historical precedents may be mentioned in the reason, but they must not determine the risk or priority by themselves.
9. If the current contract does not contain a clear risk, say "No significant risk identified."

Return ONLY valid JSON in exactly this format:

{{
  "obligation": "main obligation in the clause",
  "payment_terms": "payment terms if mentioned",
  "deadline": "deadline if mentioned",
  "risk": "main compliance or business risk",
  "priority": "high, medium, or low",
  "reason": "brief explanation of the risk"
}}
"""


response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=500
)



# Process LLM response

answer = response.choices[0].message.content

print("\nRAW LLM RESPONSE:")
print(answer)


result = json.loads(
    answer.replace("```json", "")
          .replace("```", "")
          .strip()
)


print("\nAI Agent Response:")
print(json.dumps(result, indent=2))
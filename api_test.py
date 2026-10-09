import requests
import json
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)
def get_cik_from_ticker(ticker):

    url = "https://www.sec.gov/files/company_tickers.json"

    response = requests.get(
        url,
        headers={
            "User-Agent": "AI-Bootcamp student contact@example.com"
        }
    )

    companies = response.json()

    for company in companies.values():
        if company["ticker"] == ticker.upper():
            return str(company["cik_str"]).zfill(10)

    return None
def get_company_info(cik):

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    response = requests.get(
        url,
        headers={
            "User-Agent": "AI-Bootcamp student contact@example.com"
        }
    )

    data = response.json()

    return {
    "name": data["name"],
    "ticker": data["tickers"][0],
    "exchange": data["exchanges"][0],
    "industry": data["sicDescription"],
    "state": data["stateOfIncorporationDescription"]
    }

def company_background_tool(ticker):

    cik = get_cik_from_ticker(ticker)

    if cik is None:
        return {
            "error": f"Company not found for ticker: {ticker}"
        }

    return get_company_info(cik)


company = get_company_info("0000320193")

ticker = input("Enter company ticker: ")

company = company_background_tool(ticker)

print("\nCompany Background:")
print(json.dumps(company, indent=2))


cik = get_cik_from_ticker(ticker)

print("CIK:", cik)

company = get_company_info(cik)
contract_clause = """
The vendor must deliver 500 units every month.
Deliveries must be completed by the last business day of each month.
"""
llm_request = {
    "company": company,
    "contract_clause": contract_clause,
    "task": "Analyze the contract clause for compliance risks using the company information as context."
}

print("\nJSON sent to LLM:")
print(json.dumps(llm_request, indent=2))
prompt = f"""
You are a contract compliance assistant.

Analyze this contract clause using the company information as context.

Company information:
{json.dumps(company, indent=2)}

Contract clause:
{contract_clause}

Return a short explanation of any important compliance risk.
"""

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=300
)

print("\nLLM Response:")
print(response.choices[0].message.content)
print("\nCompany Profile:")
print(json.dumps(company, indent=2))
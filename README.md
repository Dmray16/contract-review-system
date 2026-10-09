
# Contract Review System

An educational AI bootcamp project exploring contract analysis and multi-agent workflows.

## Features

- **Contract analysis:** Splits contract text into manageable chunks.
- **Compliance checks:** Identifies potential delivery, payment, and termination obligations using simple rules.
- **Risk classification:** Assigns basic risk levels based on detected keywords.
- **Multi-agent workflow:** Orchestrates three processing stages with LangGraph.
- **Interactive interface:** Allows users to submit contracts through Streamlit.
- **Docker:** Runs the application in a container.

## Technologies

- Python
- LangGraph
- Streamlit
- Docker
- ChromaDB (RAG experiment)
- SEC company data API (background-check experiment)

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   streamlit run app.py
   ```

## Run with Docker

Build the image:

```bash
docker build -t contract-review .
```

Start the container:

```bash
docker run --rm -p 127.0.0.1:8501:8501 contract-review
```

Open http://localhost:8501 in your browser.

## Limitations

This is a learning prototype, not a production legal tool. Its current risk classifications are rule-based and may be inaccurate. It does not replace review by a qualified legal professional.

The RAG and SEC API experiments are separate from the current Streamlit workflow.

## Security

Do not submit confidential contracts or sensitive personal information. Keep API keys and other secrets out of source control.
# customer-support-AI

Working MVP for a lightweight customer support AI with:
- query classification (`Billing`, `Technical`, `Account Access`)
- TF-IDF retrieval over local Markdown knowledge base
- grounded answer generation with OpenAI SDK
- low-confidence / out-of-scope escalation with reason
- Streamlit chat UI

## Project structure

- `/home/runner/work/customer-support-AI/customer-support-AI/app.py`
- `/home/runner/work/customer-support-AI/customer-support-AI/requirements.txt`
- `/home/runner/work/customer-support-AI/customer-support-AI/.env.example`
- `/home/runner/work/customer-support-AI/customer-support-AI/data/knowledge_base.md`
- `/home/runner/work/customer-support-AI/customer-support-AI/src/classifier.py`
- `/home/runner/work/customer-support-AI/customer-support-AI/src/retriever.py`
- `/home/runner/work/customer-support-AI/customer-support-AI/src/generator.py`
- `/home/runner/work/customer-support-AI/customer-support-AI/src/escalation.py`
- `/home/runner/work/customer-support-AI/customer-support-AI/src/pipeline.py`
- `/home/runner/work/customer-support-AI/customer-support-AI/tests/test_pipeline.py`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI key in `.env`:

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
```

## Run app

```bash
streamlit run app.py
```

## Run tests

```bash
pytest -q
```

## Example demo queries

1. Billing: `I was charged twice for my subscription.`
2. Technical: `My application keeps returning a 500 error.`
3. Out-of-scope: `Can you tell me today's weather in Guntur?`

Expected behavior:
- Billing and Technical return grounded answers with source titles.
- Out-of-scope query triggers visible escalation with rationale.

# AI Job Insight Assistant

[![Live Demo](https://img.shields.io/badge/Live_Demo-Open_App-FF4B4B?logo=streamlit&logoColor=white)](https://zhang-jin-ai-job-insight.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered portfolio project that converts unstructured job descriptions into structured requirements, evidence-based resume matching, capability gaps, and role-specific interview preparation.

**[Try the live demo →](https://zhang-jin-ai-job-insight.streamlit.app/)**

**Product & AI Portfolio Project by ZHANG JIN**

## Why This Product

Candidates often spend significant time reading repetitive job descriptions, comparing similar roles, and deciding how their experience maps to each requirement. Generic chatbots may summarize a JD, but they do not consistently trace conclusions back to resume evidence or provide a repeatable comparison framework.

This project explores how structured product design and generative AI can make that workflow faster, clearer, and more reliable.

## MVP Features

- Structured JD analysis
- Role classification
- Required and preferred qualification extraction
- Evidence-based resume matching
- Three-level capability gap analysis
- Role-specific interview question generation
- Downloadable Markdown report
- Local demo mode that works without an API key
- Optional OpenAI Structured Outputs mode

## Product Documentation

- [Product Requirements Document](docs/PRD.md)
- [User Flow](docs/user-flow.md)

## Product Decisions

### Evidence before scores

Every strong or partial match must contain evidence from the supplied resume. When evidence is unavailable, the product reports a capability gap instead of fabricating experience.

### Useful without an API key

Local Demo mode uses transparent rules for role classification, requirement extraction, and resume evidence matching. This lets reviewers run the MVP immediately.

### Structured AI output

The optional AI mode uses a typed Pydantic schema and the OpenAI Responses API so the user interface receives consistent fields instead of unrestricted prose.

### Privacy by default

The MVP does not intentionally save JD or resume content. API keys must be entered at runtime or supplied through environment variables and must never be committed to GitHub.

## Technology Stack

- Python
- Streamlit
- pandas
- Pydantic
- OpenAI Responses API
- Structured Outputs

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jeffreyzhjin/ai-job-insight-assistant.git
cd ai-job-insight-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

The application opens in Local Demo mode and does not require an API key.

## Optional OpenAI Mode

Set the API key in the environment before starting the application.

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_MODEL="gpt-5.6-luna"
streamlit run app.py
```

macOS or Linux:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-5.6-luna"
streamlit run app.py
```

Do not put a real API key in source code, screenshots, or committed files.

## Evaluation Plan

The MVP will be evaluated with job descriptions from product, operations, business analysis, and strategy roles.

| Metric | Initial Target |
|---|---:|
| Requirement extraction accuracy | ≥ 90% |
| Resume evidence accuracy | ≥ 85% |
| Unsupported evidence rate | ≤ 5% |
| User usefulness rating | ≥ 4/5 |
| Manual analysis time reduction | ≥ 60% |

These are initial product targets, not validated performance claims. Results will be added after testing.

## Repository Structure

```text
.
├── app.py
├── analysis_engine.py
├── requirements.txt
├── docs/
│   ├── PRD.md
│   └── user-flow.md
└── tests/
    └── test_local_engine.py
```

## Roadmap

- [x] Product requirements document
- [x] User flow
- [x] Local demonstration engine
- [x] OpenAI structured analysis integration
- [ ] Multi-role comparison
- [ ] PDF and DOCX resume upload
- [ ] Application tracking dashboard
- [ ] Evaluation dataset and test report
- [ ] Public deployment

## Responsible AI Notes

- Results are decision support, not final application decisions.
- Users should verify extracted requirements against the original JD.
- Resume evidence must never be invented.
- Sensitive personal information should be removed before analysis.
- Model outputs may contain errors even when the JSON structure is valid.

## License

This project is released under the MIT License.

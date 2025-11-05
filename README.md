
## HerLens — Knowledge-Graph-Driven Biological Q&A Assistant ##

HerLens is a women’s-health–focused assistant powered by a verified biomedical knowledge graph (KG). The graph integrates diseases, genes, proteins, biomarkers, treatments, and drugs into a unified structure sourced from trusted molecular and clinical repositories.

By grounding responses in curated relationships, HerLens offers aggregated, traceable answers and reduces hallucination. When data is missing from the KG, the system temporarily falls back to OpenAI to maintain continuity.

The long-term goal is to expand the KG with richer validated data so that HerLens can operate with higher accuracy and less dependence on general LLMs—ultimately becoming a more precise, trustworthy tool for women’s-health exploration.


---

## Why a Knowledge Graph?

Biological information is interconnected, hierarchical, and fragmented.
Traditional LLMs can synthesize language but may hallucinate molecular relationships. A curated KG fixes this problem.

Advantages of HerLens’ KG-based approach:

• **Biological accuracy** — All answers are backed by structured, curated relationships

• **Transparent provenance** — Diseases, genes, drugs, biomarkers, and treatments are verifiably linked

• **Reduced hallucination** — The KG constrains outputs to known biological edges

• **Structured aggregation** — HerLens returns complete sets (e.g., “all biomarkers for Endometriosis”)

• **Interoperability** — JSON-based data can be extended with domain-specific ontologies

• **Bidirectional lookups** — Supports disease→gene and gene→disease queries


This makes HerLens ideal for research workflows, education, data enrichment, and early-stage clinical knowledge exploration.

---

## Features

## AI-powered Q&A
• Aggregated answers drawn directly from the KG

• Entity-aware parsing for conditions, genes, biomarkers, drugs, proteins, and therapies

• Fallback intelligence via OpenAI/Hugging Face when KG has no matching data

## Clean, approachable interface ##
• Single-topic Q&A chat flow

• Sample prompts beneath search

• Professional aesthetic design

## Knowledge-graph consistency ##
• Self-checks to reduce broken links or missing nodes

• Unified querying for:
Disease → Genes / Proteins / Biomarkers / Treatments / Drugs


## Quick Start

### Prerequisites

• Python 3.9+

• pip

• Optional: OpenAI API key

• Optional: Hugging Face API key

### Installation

```
git clone https://github.com/<your-username>/HerLens.git
cd HerLens
```

(Recommended) create virtual environment:

```
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
HF_API_KEY=hf-...
HF_MODEL=bigscience/bloomz-560m
KG_MODE=1
```

KG_MODE=1 ensures the KG is used as primary data.

---

## Run the App

```
uvicorn herlens_app:app --reload

```

Open in browser:
[http://localhost:8000](http://localhost:8000)

---

## Usage Examples

• “What treatments are available for Polycystic Ovary Syndrome?”

• “What are the genes associated with Ovarian Cancer?”

• “What is the survival rate for women suffering from Stage-4 Breast cancer?”

HerLens returns **structured, consolidated lists** using KG first, and only falls back to LLMs when needed.

---

## Knowledge Graph Data

Entities:

• Diseases (e.g., Endometriosis, Breast Cancer, Preeclampsia)

• Genes

• Proteins

• Biomarkers

• Treatments

• Drugs


Relationships:

• associated_with

• biomarker_of

• treated_with

• uses_drug

• drug_used

• encodes


Place your curated `knowledge_graph.json` at the project root.

---

## Project Structure

```
HerLens/
├── herlens_app.py           # FastAPI backend with KG logic
├── knowledge_graph.json     # Curated biomedical graph
├── requirements.txt         # Dependencies
├── .env                     # Environment variables (not committed)
├── static/                  # UI styling
│   └── style.css
├── templates/
│   └── index.html           # UI + search/examples
└── README.md
```

---

## Tech Stack

Backend — FastAPI, Uvicorn

Data — JSON-based Knowledge Graph

AI Integration — OpenAI (optional), Hugging Face (optional)

Frontend — HTML/CSS/JS

---

## Advanced Features

## KG Query Engine: ##

• Disease → Genes / Proteins / Biomarkers / Treatments / Drugs

• Gene ↔ Protein

• Biomarker → Disease

• Treatment / Drug → Disease


## Graceful fallbacks: ##

• LLM lookups only when KG lacks a direct biological edge


## Consistent formatting: ##

• Clean, aggregated results for each entity query

---

## Configuration Notes

• Ensure `KG_MODE=1` is set

• `knowledge_graph.json` should maintain: Top-level nodes & edges

• Nodes: id, label, type

• Edges: source, target, type

---

## Troubleshooting

• “Internal server error: 'Treatment:Hormonal suppression'”
→ Add node or update name to match an existing treatment


• Aggregation returns 1 item
→ Verify edges correctly connect Disease→target


• JSON formatting errors
→ Auto-format (VS Code) or validate with `json.load()`


---

## Author

**Sthavitha Rithu LNS** - Concept, curation, and implementation

---

## Support

If you run into issues:

• Check `.env`

• Validate `knowledge_graph.json`

• Inspect terminal logs

---

## Future Enhancements

• Disease-level summaries when entity type omitted

• UI usability refinements

• Expanded KG coverage for additional conditions

• Optional Docker render templates

• Lightweight graph visualization


HerLens aims to bring rigor and clarity to women’s-health questions through **validated biological graph knowledge**, augmented by modern AI models.

---



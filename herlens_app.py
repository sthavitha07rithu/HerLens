import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "bigscience/bloomz-560m")

KG_MODE = os.getenv("KG_MODE", "0") == "1"
KG_PATH = os.path.join(os.path.dirname(__file__), "knowledge_graph.json")

# OpenAI client (optional)
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except Exception:
    client = None

app = FastAPI()
BASE_DIR = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- Load Knowledge Graph ---
KG_NODES = {}
KG_EDGES = []


def load_kg():
    global KG_NODES, KG_EDGES
    try:
        with open(KG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            nodes = data.get("nodes", [])
            edges = data.get("edges", [])

            # Build node dictionary
            KG_NODES = {node["id"]: {"label": node["label"], "type": node["type"]} for node in nodes}
            KG_EDGES = edges
            return True
    except Exception as e:
        print(f"Error loading KG: {e}")
        return False


KG_LOADED = load_kg()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/query")
async def query_endpoint(payload: dict):
    try:
        user_q = payload.get("query", "")
        if not user_q:
            return JSONResponse({"error": "Empty query"}, status_code=400)

        # 1. Try Knowledge Graph
        if KG_MODE and KG_LOADED:
            answer = answer_from_kg(user_q)
            if "couldn't find" not in answer.lower():
                return {"answer": f"I found this in the knowledge graph:\n{answer}"}

        # 2. Fallback to OpenAI if key present
        if OPENAI_API_KEY and client:
            try:
                resp = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[{"role": "user", "content": user_q}]
                )
                answer = resp.choices[0].message.content.strip()
                return {"answer": f"Information wasn't available in knowledge graph, but here’s what I found in OpenAI:\n{answer}"}
            except Exception as e:
                return JSONResponse({"error": f"OpenAI error: {str(e)}"}, status_code=500)

        # 3. Fallback to Hugging Face if OpenAI not available
        if HF_API_KEY:
            try:
                headers = {"Authorization": f"Bearer {HF_API_KEY}"}
                hf_payload = {"inputs": user_q}
                resp = requests.post(
                    f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}",
                    headers=headers, json=hf_payload, timeout=30
                )
                resp.raise_for_status()
                data = resp.json()
                if isinstance(data, list) and "generated_text" in data[0]:
                    answer = data[0]["generated_text"]
                else:
                    answer = str(data)
                return {
                    "source": "huggingface",
                    "answer": f"Wasn't available in knowledge graph or OpenAI, but found this on the internet: {answer}"
                }
            except Exception as e:
                return JSONResponse({"error": f"Hugging Face error: {str(e)}"}, status_code=500)

        return JSONResponse({"error": "No valid data source available."}, status_code=500)

    except Exception as e:
        return JSONResponse({"error": f"Internal server error: {str(e)}"}, status_code=500)


@app.get("/api/status")
async def status():
    return {
        "openai_key_present": bool(OPENAI_API_KEY),
        "hf_key_present": bool(HF_API_KEY),
        "kg_mode": KG_MODE,
        "knowledge_graph_loaded": KG_LOADED
    }


# --- Universal KG Query Function (aggregates all matches) ---
def answer_from_kg(query: str) -> str:
    q = query.lower()

    # --- Disease-based lookups ---
    for node_id, node in KG_NODES.items():
        if node["type"] == "Disease" and node["label"].lower() in q:
            disease_label = node["label"]

            # Collect all related entities
            genes = [KG_NODES[e["target"]]["label"] for e in KG_EDGES
                     if e["source"] == node_id and e["type"] == "associated_with" and KG_NODES[e["target"]]["type"] == "Gene"]
            proteins = [KG_NODES[e["target"]]["label"] for e in KG_EDGES
                        if e["source"] == node_id and KG_NODES[e["target"]]["type"] == "Protein"]
            biomarkers = [KG_NODES[e["target"]]["label"] for e in KG_EDGES
                          if e["source"] == node_id and e["type"] == "biomarker_of"]
            treatments = [KG_NODES[e["target"]]["label"] for e in KG_EDGES
                          if e["source"] == node_id and e["type"] == "treated_with"]
            drugs = [KG_NODES[e["target"]]["label"] for e in KG_EDGES
                     if e["source"] == node_id and KG_NODES[e["target"]]["type"] == "Drug"]

            if "gene" in q and genes:
                return f"Genes associated with {disease_label}: {', '.join(sorted(set(genes)))}"
            if "protein" in q and proteins:
                return f"Proteins linked to {disease_label}: {', '.join(sorted(set(proteins)))}"
            if "biomarker" in q and biomarkers:
                return f"Biomarkers for {disease_label}: {', '.join(sorted(set(biomarkers)))}"
            if ("treatment" in q or "therapy" in q) and treatments:
                return f"Treatments for {disease_label}: {', '.join(sorted(set(treatments)))}"
            if "drug" in q and drugs:
                return f"Drugs used for {disease_label}: {', '.join(sorted(set(drugs)))}"

    # --- Gene → Protein ---
    for node_id, node in KG_NODES.items():
        if node["type"] == "Gene" and node["label"].lower() in q:
            proteins = [KG_NODES[e["target"]]["label"] for e in KG_EDGES
                        if e["source"] == node_id and e["type"] == "encodes"]
            if proteins:
                return f"The protein(s) encoded by {node['label']} are: {', '.join(sorted(set(proteins)))}"

    # --- Protein → Gene ---
    for node_id, node in KG_NODES.items():
        if node["type"] == "Protein" and node["label"].lower() in q:
            genes = [KG_NODES[e["source"]]["label"] for e in KG_EDGES
                     if e["target"] == node_id and e["type"] == "encodes"]
            if genes:
                return f"The gene(s) encoding {node['label']} are: {', '.join(sorted(set(genes)))}"

    # --- Biomarker → Disease ---
    for node_id, node in KG_NODES.items():
        if node["type"] == "Biomarker" and node["label"].lower() in q:
            diseases = [KG_NODES[e["source"]]["label"] for e in KG_EDGES
                        if e["target"] == node_id and e["type"] == "biomarker_of"]
            if diseases:
                return f"The biomarker {node['label']} is associated with: {', '.join(sorted(set(diseases)))}"

    # --- Drug → Disease ---
    for node_id, node in KG_NODES.items():
        if node["type"] == "Drug" and node["label"].lower() in q:
            diseases = [KG_NODES[e["source"]]["label"] for e in KG_EDGES
                        if e["target"] == node_id and e["type"] in ["drug_used", "uses_drug"]]
            if diseases:
                return f"The drug {node['label']} is used in treatment of: {', '.join(sorted(set(diseases)))}"

 # --- Treatment → Disease ---
    for node_id, node in KG_NODES.items():
        if node["type"] == "Treatment" and node["label"].lower() in q:
            diseases = [
                KG_NODES[e["source"]]["label"]
                for e in KG_EDGES
                if e["target"] == node_id and e["type"] == "treated_with"
            ]
            if diseases:
                return f"The treatment {node['label']} is used for: {', '.join(sorted(set(diseases)))}"

    # --- Default fallback ---
    return "I couldn't find a direct answer in the knowledge graph."

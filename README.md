HerLens
======

Small FastAPI app that demonstrates a baby-pink frontend and a Python backend which forwards queries to OpenAI or a local Knowledge Graph JSON.

Setup
-----
1. Create a virtual environment and activate it.

   powershell:
   ```powershell
   python -m venv .venv; .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Open `.env` and paste your OpenAI API key into `OPENAI_API_KEY`. Optionally change `OPENAI_MODEL`.

4. Run the app:

   ```powershell
   uvicorn app:app --reload --port 8000
   ```

5. Open http://localhost:8000

Toggling Knowledge Graph mode
-----------------------------
- Set `KG_MODE=1` in `.env` to use `knowledge_graph.json` (lookup-based responses) instead of OpenAI.

Notes
-----
- The default model name is set via `.env` (`OPENAI_MODEL`). Use `chatgpt-5-mini` if you have access.
- This repository uses minimal JS in the frontend to keep logic in Python where possible; the JS only forwards user input to the backend and renders results.

PowerShell helper (Windows)
----------------------------
If you run into "uvicorn: The term 'uvicorn' is not recognized..." or want a single command to load `.env` and start the server using the project's virtualenv, use the included `run_server.ps1` from the repository root.

From `C:\HerLens` run:

```powershell
./run_server.ps1
```

This script will load `HerLens\\.env` into the environment for the spawned process and start the server using `.venv`'s Python so you don't need to activate the venv manually.

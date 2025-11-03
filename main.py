"""Convenience wrapper so callers can run:

    uvicorn herlens_app:app --reload

This imports the FastAPI `app` instance from the package `HerLens.app`.
"""
from fastapi import Request
from HerLens.app import app, ask  # import the ask handler or function used in the package

# If the package's ask handler is a route function named `ask` that accepts a Request,
# the alias below will delegate to it. If the handler has a different name,
# replace `ask` with the actual function name (for example `ask_endpoint`).

@app.post("/api/query")
async def api_query(request: Request):
    # Delegate to the package's ask handler so both /ask and /api/query behave the same.
    return await ask(request)

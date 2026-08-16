"""Local FastAPI application for the SynthSEA research workbench."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from synthsea.api.errors import add_error_handlers
from synthsea.api.routes import chat, evidence, intakes, training

app = FastAPI(title="SynthSEA Research Workbench", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_error_handlers(app)
app.include_router(intakes.router)
app.include_router(training.router)
app.include_router(chat.router)
app.include_router(evidence.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Report whether the local workbench API is running."""

    return {"status": "ok"}
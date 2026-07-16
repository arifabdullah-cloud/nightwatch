from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="Nightwatch Workload",
    description="Production-like workload used by the Nightwatch reliability platform.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "nightwatch-workload",
        "status": "running",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready")
def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

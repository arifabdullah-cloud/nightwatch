from datetime import datetime, timezone

from fastapi import FastAPI

from api.products import router as products_router

app = FastAPI(
    title="Nightwatch Workload",
    description=(
        "Production-like e-commerce workload used by the "
        "Nightwatch cloud reliability platform."
    ),
    version="0.1.0",
)

app.include_router(products_router)


@app.get("/", tags=["System"])
def root() -> dict[str, str]:
    return {
        "service": "nightwatch-workload",
        "status": "running",
        "version": app.version,
    }


@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready", tags=["System"])
def readiness() -> dict[str, str]:
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

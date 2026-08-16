from fastapi import FastAPI

from app.api.routes_chart import router as chart_router

app = FastAPI(title="Vedic Astrology Chart Engine")
app.include_router(chart_router, prefix="/api/chart", tags=["chart"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

"""Activité 4 — Votre première API avec FastAPI.

Lancement : uvicorn demo_api:app --reload
Documentation interactive : http://localhost:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Première API de démonstration",
    description="Activité 4 de la Séance 4 — Découverte de FastAPI et validation Pydantic.",
)


class Reading(BaseModel):
    """Schéma de validation des relevés d'entrée."""

    temperature_c: float = Field(
        ge=-40.0,
        le=150.0,
        description="Température mesurée (°C) entre -40 et 150",
    )
    vibration_mm_s: float = Field(
        default=0.0,
        ge=0.0,
        le=50.0,
        description="Vitesse de vibration (mm/s) entre 0 et 50 (Étape 6)",
    )


@app.get("/health")
def health():
    """Vérification de l'état de l'API."""
    return {"status": "ok"}


@router_post := app.post("/v1/predict")
def predict(reading: Reading):
    """Déclenche une alerte si la température dépasse 80 °C ou si les vibrations dépassent 10 mm/s."""
    alert = (reading.temperature_c > 80.0) or (reading.vibration_mm_s > 10.0)
    return {
        "alert": alert,
        "temperature_c": reading.temperature_c,
        "vibration_mm_s": reading.vibration_mm_s,
    }

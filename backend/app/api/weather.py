from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.services.weather_service import get_weather, calculate_disease_risk

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/risk")
def get_weather_and_disease_risk(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch user's village, fallback to a default if not set
    village = current_user.village or "Default Village"

    # Get weather
    weather_data = get_weather(village)

    # Calculate disease risk
    disease_risks = calculate_disease_risk(weather_data)

    return {
        "village": village,
        "weather": weather_data,
        "risks": disease_risks
    }

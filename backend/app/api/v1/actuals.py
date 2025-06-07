from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.db import get_db
from backend.app.models.actual_schemas import ActualOutcomeRequest, ActualOutcomeResponse
from backend.app.repos import actuals


router = APIRouter(prefix="/predictions/{prediction_id}/actuals", tags=["actuals"])


@router.get("", response_model=ActualOutcomeResponse)
def get_actual(prediction_id: int, db: Session = Depends(get_db)):
    actual = actuals.get_actual_by_prediction_id(db, prediction_id)
    if not actual:
        raise HTTPException(status_code=404, detail=f"Actual outcome not found by prediction ID: {prediction_id}")
    return actual


@router.put("", response_model=ActualOutcomeResponse)
def update_actual(prediction_id: int, request: ActualOutcomeRequest, db: Session = Depends(get_db)):
    new_actual = actuals.update_actual(db, prediction_id, request)
    if not new_actual:
        raise HTTPException(status_code=404, detail=f"Actual outcome not found by prediction ID: {prediction_id}")
    return new_actual

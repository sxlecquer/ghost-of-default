from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.db import get_db
from backend.app.models.prediction_schemas import PredictionRequest, PredictionResponse
from backend.app.models.common_schemas import PaginationParams
from backend.app.repos import predictions


router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/{id}", response_model=PredictionResponse)
async def get_prediction(id: int, db: Session = Depends(get_db)):
    pred = predictions.get_prediction_by_id(db, id)
    if not pred:
        raise HTTPException(status_code=404, detail=f"Prediction not found by ID: {id}")
    return predictions.map_entity_to_response(pred)


@router.get("", response_model=list[PredictionResponse])
async def search_predictions(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    entities = predictions.get_all_predictions(db, pagination.page_num, pagination.page_size)
    return [predictions.map_entity_to_response(ent) for ent in entities]


@router.post("", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(request: PredictionRequest, db: Session = Depends(get_db)):
    pred = predictions.create_prediction(db, request)
    return predictions.map_entity_to_response(pred)


@router.put("/{id}", response_model=PredictionResponse)
async def update_prediction(id: int, request: PredictionRequest, db: Session = Depends(get_db)):
    new_pred = predictions.update_prediction(db, id, request)
    if not new_pred:
        raise HTTPException(status_code=404, detail=f"Prediction not found by ID: {id}")
    return predictions.map_entity_to_response(new_pred)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction(id: int, db: Session = Depends(get_db)):
    success = predictions.delete_prediction(db, id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Prediction not found by ID: {id}")

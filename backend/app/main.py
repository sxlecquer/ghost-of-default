from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.db import create_db_tables, get_db
from backend.app.models.prediction_schemas import PredictionRequest, PredictionResponse
from backend.app.models.common_schemas import PaginationParams
from backend.app.repos import predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/predictions/{id}", response_model=PredictionResponse)
async def get_prediction(id: int, db: Session = Depends(get_db)):
    pred = predictions.get_prediction_by_id(db, id)
    if not pred:
        raise HTTPException(status_code=404, detail=f"Default prediction not found by ID: {id}")
    return predictions.map_entity_to_response(pred)


@app.get("/predictions", response_model=list[PredictionResponse])
async def search_predictions(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    entities = predictions.get_all_predictions(db, pagination.page_num, pagination.page_size)
    return [predictions.map_entity_to_response(ent) for ent in entities]


@app.post("/predictions", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(request: PredictionRequest, db: Session = Depends(get_db)):
    pred = predictions.create_prediction(db, request)
    return predictions.map_entity_to_response(pred)


@app.put("/predictions/{id}", response_model=PredictionResponse)
async def update_prediction(id: int, request: PredictionRequest, db: Session = Depends(get_db)):
    new_pred = predictions.update_prediction(db, id, request)
    if not new_pred:
        raise HTTPException(status_code=404, detail=f"Default prediction not found by ID: {id}")
    return predictions.map_entity_to_response(new_pred)


@app.delete("/predictions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction(id: int, db: Session = Depends(get_db)):
    success = predictions.delete_prediction(db, id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Default prediction not found by ID: {id}")

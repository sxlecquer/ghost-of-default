from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.db import create_db_tables, get_db
from backend.app.models.prediction_schemas import BankClientRequest, BankClientResponse
from backend.app.models.common_schemas import PaginationParams
from backend.app.repos import predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/clients/{id}", response_model=BankClientResponse)
async def get_client(id: int, db: Session = Depends(get_db)):
    pred = predictions.get_prediction_by_id(db, id)
    if not pred:
        raise HTTPException(status_code=404, detail=f"Client prediction not found by ID: {id}")
    return predictions.map_entity_to_response(pred)


@app.get("/clients", response_model=list[BankClientResponse])
async def search_clients(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    entities = predictions.get_all_predictions(db, pagination.page_num, pagination.page_size)
    return [predictions.map_entity_to_response(ent) for ent in entities]


@app.post("/clients", response_model=BankClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(request: BankClientRequest, db: Session = Depends(get_db)):
    pred = predictions.create_prediction(db, request)
    return predictions.map_entity_to_response(pred)


@app.put("/clients/{id}", response_model=BankClientResponse)
async def update_client(id: int, request: BankClientRequest, db: Session = Depends(get_db)):
    new_pred = predictions.update_prediction(db, id, request)
    if not new_pred:
        raise HTTPException(status_code=404, detail=f"Client prediction not found by ID: {id}")
    return predictions.map_entity_to_response(new_pred)


@app.delete("/clients/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id: int, db: Session = Depends(get_db)):
    success = predictions.delete_prediction(db, id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Client prediction not found by ID: {id}")

from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.db_models import BankClientActual
from backend.app.models.actual_schemas import ActualResultRequest
from backend.app.repos import predictions


def get_actual_by_prediction_id(db: Session, prediction_id: int) -> Optional[BankClientActual]:
    return (
        db.query(BankClientActual)
          .filter(BankClientActual.prediction_id == prediction_id)
          .first()
    )


def get_all_actuals(db: Session, page_num: int, page_size: int) -> list[BankClientActual]:
    offset = (page_num - 1) * page_size
    return db.query(BankClientActual).offset(offset).limit(page_size).all() # type: ignore


def create_actual(db: Session, prediction_id: int, request: ActualResultRequest) -> Optional[BankClientActual]:
    parent = predictions.get_prediction_by_id(db, prediction_id)
    if parent is None:
        return None

    existing = get_actual_by_prediction_id(db, prediction_id)
    if existing is not None:
        raise ValueError(f"Actual record already exists for prediction ID: {prediction_id}")


    actual_entity = BankClientActual(prediction_id=prediction_id, actual_default=request.actual_default)
    db.add(actual_entity)
    db.commit()
    db.refresh(actual_entity)
    return actual_entity


def update_actual(db: Session, prediction_id: int, request: ActualResultRequest) -> Optional[BankClientActual]:
    actual_entity = get_actual_by_prediction_id(db, prediction_id)
    if actual_entity is None:
        return None

    actual_entity.actual_default = request.actual_default
    db.commit()
    db.refresh(actual_entity)
    return actual_entity


def delete_actual(db: Session, prediction_id: int) -> bool:
    actual_entity = get_actual_by_prediction_id(db, prediction_id)
    if actual_entity is None:
        return False

    db.delete(actual_entity)
    db.commit()
    return True

from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.db_models import BankClientActual
from backend.app.models.actual_schemas import ActualResultRequest


def init_actual(db: Session, prediction_id: int) -> BankClientActual:
    shell = BankClientActual(prediction_id=prediction_id)
    db.add(shell)
    db.commit()
    db.refresh(shell)
    return shell


def get_actual_by_prediction_id(db: Session, prediction_id: int) -> Optional[BankClientActual]:
    return (
        db.query(BankClientActual)
          .filter(BankClientActual.prediction_id == prediction_id)
          .first()
    )


def update_actual(db: Session, prediction_id: int, request: ActualResultRequest) -> Optional[BankClientActual]:
    actual_entity = get_actual_by_prediction_id(db, prediction_id)
    if actual_entity is None:
        return None

    actual_entity.actual_default = request.actual_default
    db.commit()
    db.refresh(actual_entity)
    return actual_entity

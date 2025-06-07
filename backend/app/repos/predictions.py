from typing import Optional, cast
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session
from backend.app.models.db_models import Prediction, Sex, Education, Marriage
from backend.app.models.prediction_schemas import PredictionRequest, PredictionResponse
from backend.app.services.predictor import predict_default
from backend.app.repos import actuals


def _get_or_create_fk(db: Session, entity, name: str):
    instance = db.query(entity).filter(cast(ColumnElement, entity.name) == name).first()
    if instance is None:
        instance = entity(name=name)
        db.add(instance)
        db.commit()
        db.refresh(instance)

    return instance


def _map_request_to_entity(db: Session, request: PredictionRequest, *, default: bool, confidence: float) -> Prediction:
    data = request.model_dump()

    return Prediction(
        sex_id=_get_or_create_fk(db, Sex, data["sex"]).id,
        education_id=_get_or_create_fk(db, Education, data["education"]).id,
        marriage_id=_get_or_create_fk(db, Marriage, data["marriage"]).id,
        default=default,
        confidence=confidence,
        **{k: v for k, v in data.items() if k not in ("sex", "education", "marriage")}
    )


def map_entity_to_response(pred_entity: Prediction) -> PredictionResponse:
    data = {
        col: getattr(pred_entity, col)
        for col in pred_entity.__table__.columns.keys()
        if col not in ("sex_id", "education_id", "marriage_id")
    }

    data["sex"] = pred_entity.sex.name
    data["education"] = pred_entity.education.name
    data["marriage"] = pred_entity.marriage.name

    return PredictionResponse(**data)


def get_prediction_by_id(db: Session, prediction_id: int) -> Optional[Prediction]:
    return (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )


def get_all_predictions(db: Session, page_num: int, page_size: int) -> list[Prediction]:
    offset = (page_num - 1) * page_size
    return db.query(Prediction).offset(offset).limit(page_size).all() # type: ignore


def create_prediction(db: Session, request: PredictionRequest) -> Prediction:
    default_flag, confidence = predict_default(request)
    pred_entity = _map_request_to_entity(db, request, default=default_flag, confidence=confidence)

    db.add(pred_entity)
    db.commit()
    db.refresh(pred_entity)

    actuals.init_actual(db, pred_entity.id)

    return pred_entity


def update_prediction(db: Session, prediction_id: int, request: PredictionRequest) -> Optional[Prediction]:
    pred_entity = get_prediction_by_id(db, prediction_id)
    if pred_entity is None:
        return None

    default_flag, confidence = predict_default(request)
    updated_entity = _map_request_to_entity(db, request, default=default_flag, confidence=confidence)

    for attr in updated_entity.__table__.columns.keys():
        if attr != "id":
            setattr(pred_entity, attr, getattr(updated_entity, attr))

    db.commit()
    db.refresh(pred_entity)
    return pred_entity


def delete_prediction(db: Session, prediction_id: int) -> bool:
    pred_entity = get_prediction_by_id(db, prediction_id)
    if pred_entity is None:
        return False

    db.delete(pred_entity)
    db.commit()
    return True

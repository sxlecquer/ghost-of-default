import pandas as pd
from backend.ml import model_workflow
from backend.app.models.prediction_schemas import PredictionRequest


model = model_workflow.load_model()


def predict_default(request: PredictionRequest) -> tuple[bool, float]:
    data_dict = request.model_dump()

    for key, value in data_dict.items():
        if hasattr(value, "code"):
            data_dict[key] = value.code

    df = pd.DataFrame([data_dict])

    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0]

    default_flag = bool(pred == 1)
    confidence_score = float(proba[1] if default_flag else proba[0])

    return default_flag, confidence_score

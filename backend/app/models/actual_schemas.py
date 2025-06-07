from pydantic import BaseModel


class ActualOutcomeRequest(BaseModel):
    actual_default: bool


class ActualOutcomeResponse(ActualOutcomeRequest):
    prediction_id: int

    model_config = {
        "from_attributes": True
    }

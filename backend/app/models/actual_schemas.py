from pydantic import BaseModel


class ActualResultRequest(BaseModel):
    actual_default: bool


class ActualResultResponse(ActualResultRequest):
    prediction_id: int

    model_config = {
        "from_attributes": True
    }

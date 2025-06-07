from typing import Optional
from pydantic import BaseModel


class ActualOutcomeRequest(BaseModel):
    actual_default: bool


class ActualOutcomeResponse(ActualOutcomeRequest):
    prediction_id: int
    actual_default: Optional[bool]

    model_config = {
        "from_attributes": True
    }

from backend.app.models.enums import Sex, Education, Marriage
from pydantic import BaseModel, PositiveInt, Field


class PredictionRequest(BaseModel):
    limit_bal: PositiveInt
    sex: Sex
    education: Education
    marriage: Marriage
    age: PositiveInt

    repay_status_1: int = Field(ge=-1, le=9)
    repay_status_2: int = Field(ge=-1, le=9)
    repay_status_3: int = Field(ge=-1, le=9)
    repay_status_4: int = Field(ge=-1, le=9)
    repay_status_5: int = Field(ge=-1, le=9)
    repay_status_6: int = Field(ge=-1, le=9)

    bill_amount_1: float = Field(ge=0)
    bill_amount_2: float = Field(ge=0)
    bill_amount_3: float = Field(ge=0)
    bill_amount_4: float = Field(ge=0)
    bill_amount_5: float = Field(ge=0)
    bill_amount_6: float = Field(ge=0)

    pay_amount_1: float = Field(ge=0)
    pay_amount_2: float = Field(ge=0)
    pay_amount_3: float = Field(ge=0)
    pay_amount_4: float = Field(ge=0)
    pay_amount_5: float = Field(ge=0)
    pay_amount_6: float = Field(ge=0)


class PredictionResponse(PredictionRequest):
    id: int
    default: bool
    confidence: float

    model_config = {
        "from_attributes": True
    }

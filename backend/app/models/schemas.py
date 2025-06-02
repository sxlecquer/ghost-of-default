from enum import Enum
from pydantic import BaseModel, PositiveInt, Field


class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"

    @property
    def code(self) -> int:
        return {
            "male": 1,
            "female": 2
        }[self.value]


class Education(str, Enum):
    GRADUATE_SCHOOL = "graduate_school"
    UNIVERSITY = "university"
    HIGH_SCHOOL = "high_school"
    OTHERS = "others"

    @property
    def code(self) -> int:
        return {
            "graduate_school": 1,
            "university": 2,
            "high_school": 3,
            "others": 4
        }[self.value]


class Marriage(str, Enum):
    MARRIED = "married"
    SINGLE = "single"
    OTHERS = "others"

    @property
    def code(self) -> int:
        return {
            "married": 1,
            "single": 2,
            "others": 3
        }[self.value]


class PaginationParams(BaseModel):
    page_num: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)


class BankClientRequest(BaseModel):
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


class BankClientResponse(BankClientRequest):
    id: int
    default: bool
    confidence: float

    model_config = {
        "from_attributes": True
    }

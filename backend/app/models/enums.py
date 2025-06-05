from enum import Enum


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

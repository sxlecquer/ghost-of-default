from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Sex(Base):
    __tablename__ = "sex_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Education(Base):
    __tablename__ = "education_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Marriage(Base):
    __tablename__ = "marriage_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    limit_bal = Column(Integer, nullable=False)
    sex_id = Column(Integer, ForeignKey("sex_types.id"), nullable=False)
    education_id = Column(Integer, ForeignKey("education_types.id"), nullable=False)
    marriage_id = Column(Integer, ForeignKey("marriage_types.id"), nullable=False)
    age = Column(Integer, nullable=False)

    repay_status_1 = Column(Integer, nullable=False)
    repay_status_2 = Column(Integer, nullable=False)
    repay_status_3 = Column(Integer, nullable=False)
    repay_status_4 = Column(Integer, nullable=False)
    repay_status_5 = Column(Integer, nullable=False)
    repay_status_6 = Column(Integer, nullable=False)

    bill_amount_1 = Column(Float, nullable=False)
    bill_amount_2 = Column(Float, nullable=False)
    bill_amount_3 = Column(Float, nullable=False)
    bill_amount_4 = Column(Float, nullable=False)
    bill_amount_5 = Column(Float, nullable=False)
    bill_amount_6 = Column(Float, nullable=False)

    pay_amount_1 = Column(Float, nullable=False)
    pay_amount_2 = Column(Float, nullable=False)
    pay_amount_3 = Column(Float, nullable=False)
    pay_amount_4 = Column(Float, nullable=False)
    pay_amount_5 = Column(Float, nullable=False)
    pay_amount_6 = Column(Float, nullable=False)

    default = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)

    sex = relationship("Sex")
    education = relationship("Education")
    marriage = relationship("Marriage")

    actual_outcome = relationship(
        "ActualOutcome",
        uselist=False,
        back_populates="prediction",
        cascade="all, delete-orphan"
    )


class ActualOutcome(Base):
    __tablename__ = "actual_outcomes"

    prediction_id = Column(Integer, ForeignKey("predictions.id"), primary_key=True, index=True)
    actual_default = Column(Boolean, nullable=True, default=None)

    prediction = relationship(
        "Prediction",
        back_populates="actual_outcome",
        uselist=False
    )

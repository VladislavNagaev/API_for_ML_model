from typing import Literal
from pydantic import BaseModel, Field


class AnswerData(BaseModel):
    class_predicted: Literal["Yes", "No"] = Field(alias='Churn')
    probability: float = Field(alias='Probability', ge=0, le=1)

from typing import Literal
from pydantic import BaseModel, Field


class PredictionData(BaseModel):
    param_1: int = Field(
        alias='SeniorCitizen', ge=0, le=1, 
        description='Must be 0 or 1!')
    param_2: Literal["Yes", "No"] = Field(alias='Dependents')
    param_3: int = Field(
        alias='tenure', ge=0, le=72, description='Must be between 0 and 72!')
    param_4: Literal["Yes", "No"] = Field(alias='PhoneService')
    param_5: Literal["Yes", "No", "No phone service"] = Field(
        alias='MultipleLines')
    param_6: Literal["Fiber optic", "DSL", "No"] = Field(
        alias='InternetService')
    param_7: Literal["Yes", "No", "No internet service"] = Field(
        alias='OnlineSecurity')
    param_8: Literal["Yes", "No", "No internet service"] = Field(
        alias='OnlineBackup')
    param_9: Literal["Yes", "No", "No internet service"] = Field(
        alias='DeviceProtection')
    param_10: Literal["Yes", "No", "No internet service"] = Field(
        alias='TechSupport')
    param_11: Literal["Month-to-month", "One year", "Two year"] = Field(
        alias='Contract')
    param_12: float = Field(
        alias='MonthlyCharges', ge=18.25, le=118.75, 
        description='Must be between 18.25 and 118.75!'
    )

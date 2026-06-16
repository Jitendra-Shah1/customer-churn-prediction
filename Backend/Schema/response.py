from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="Predicted class: 0 or 1")
    probability: float = Field(..., description="Probability of churn (class 1)")
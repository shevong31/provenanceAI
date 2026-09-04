from pydantic import BaseModel
from typing import Optional, List, Any

# Data expected when submitting an essay
class SubmissionCreate(BaseModel):
    student_id: int
    essay_text: str

# Data returned back to the frontend
class SubmissionResponse(BaseModel):
    id: int
    student_id: int
    status: str
    anomaly_score: Optional[float] = None

    class Config:
        from_attributes = True
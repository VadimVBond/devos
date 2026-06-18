import uuid
from typing import Literal
from pydantic import BaseModel, Field

class FeedbackPattern(BaseModel):
    pattern_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Literal["failure", "success", "warning"]
    severity: Literal["low", "medium", "high"]
    source_task: str
    action: str
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)
    
    # Store stringified parameters or specific keys to help matching
    context_signature: str = ""

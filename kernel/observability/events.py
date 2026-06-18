from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

class BaseEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    event_type: str

class TaskStarted(BaseEvent):
    event_type: str = "TaskStarted"
    graph_id: str
    task_id: int
    action: str
    input_data: Dict[str, Any]

class TaskCompleted(BaseEvent):
    event_type: str = "TaskCompleted"
    graph_id: str
    task_id: int
    action: str
    output_data: Dict[str, Any]
    duration_ms: float

class TaskFailed(BaseEvent):
    event_type: str = "TaskFailed"
    graph_id: str
    task_id: int
    action: str
    error: str
    duration_ms: float

class TaskSkipped(BaseEvent):
    event_type: str = "TaskSkipped"
    graph_id: str
    task_id: int
    reason: str

class GraphStarted(BaseEvent):
    event_type: str = "GraphStarted"
    graph_id: str
    intent: str

class GraphCompleted(BaseEvent):
    event_type: str = "GraphCompleted"
    graph_id: str
    duration_ms: float
    status: str

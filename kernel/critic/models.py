from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from kernel.planner import ExecutionPlan, ExecutionGraph

class DecisionTraceItem(BaseModel):
    rule: str
    result: str  # "passed" or "failed"
    details: Optional[str] = None

class CriticReview(BaseModel):
    status: str  # "approved", "rejected", "modified"
    reasoning: str
    original_graph: ExecutionGraph
    final_graph: ExecutionGraph
    issues: List[str] = Field(default_factory=list)
    optimizations: List[str] = Field(default_factory=list)
    decision_trace: List[DecisionTraceItem] = Field(default_factory=list)

    def add_trace(self, rule: str, result: str, details: str = None):
        self.decision_trace.append(DecisionTraceItem(rule=rule, result=result, details=details))

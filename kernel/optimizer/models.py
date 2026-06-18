from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from kernel.planner import ExecutionGraph

class OptimizedExecutionGraph(BaseModel):
    """
    Финальный граф выполнения, подготовленный для KernelExecutor.
    Гарантирует стабильность пакетирования и детерминизм.
    """
    original_graph: ExecutionGraph
    optimized_graph: ExecutionGraph
    
    # Список пакетов, где каждый пакет (батч) - список ID узлов для параллельного выполнения.
    # Batch N выполняется строго после полного завершения Batch N-1.
    execution_batches: List[List[int]] = Field(default_factory=list)
    
    cost_analysis: Dict[str, Any] = Field(default_factory=dict)
    performance_score: float = 1.0
    changes_log: List[str] = Field(default_factory=list)
    
    bottlenecks: List[str] = Field(default_factory=list)
    execution_risk: str = "low"

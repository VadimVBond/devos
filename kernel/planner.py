import json
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from ai.runtime import AIRuntime

class TaskNode(BaseModel):
    id: int
    action: str
    input: Dict[str, Any] = Field(default_factory=dict)
    max_retries: int = 0

class ExecutionGraph(BaseModel):
    nodes: List[TaskNode] = Field(default_factory=list)
    edges: List[Tuple[int, int]] = Field(default_factory=list)  # (from_id, to_id)

class ExecutionPlan(BaseModel):
    intent: str
    graph: ExecutionGraph = Field(default_factory=ExecutionGraph)
    risk_level: str = "low"
    requires_confirmation: bool = True

class KernelPlanner:
    """
    Планировщик DevOS Kernel.
    Генерирует направленный ациклический граф (DAG) задач.
    """
    
    def __init__(self, runtime: AIRuntime = None):
        self.runtime = runtime or AIRuntime()

    async def plan(self, intent: str) -> ExecutionPlan:
        """
        Преобразует интент пользователя в структурированный граф задач.
        """
        try:
            # Вызов AI Runtime для получения структуры графа
            raw_response = await self.runtime.execute_structured(
                prompt_name="DEVOS KERNEL PROMPT", 
                user_input=intent
            )
            
            # В будущем здесь будет парсинг реального JSON-ответа в ExecutionPlan
            # Пока создаем пустой граф-заглушку
            return ExecutionPlan(
                intent=intent,
                graph=ExecutionGraph(nodes=[], edges=[]),
                risk_level="low",
                requires_confirmation=False
            )
        except Exception as e:
            from loguru import logger
            logger.error(f"Planning failed: {e}")
            raise

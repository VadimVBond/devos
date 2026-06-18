import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from ai.runtime import AIRuntime

class TaskStep(BaseModel):
    id: int
    action: str
    input: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[int] = Field(default_factory=list)

class ExecutionPlan(BaseModel):
    intent: str
    tasks: List[TaskStep]
    risk_level: str  # low | medium | high
    requires_confirmation: bool = True

class KernelPlanner:
    """
    Детерминированный планировщик DevOS Kernel.
    Использует AIRuntime для получения когнитивных решений.
    """
    
    def __init__(self, runtime: AIRuntime = None):
        self.runtime = runtime or AIRuntime()

    async def plan(self, intent: str) -> ExecutionPlan:
        """
        Преобразует интент пользователя в структурированный граф задач
        используя AI Runtime и когнитивные инструкции.
        """
        # Вызываем AI Runtime с промптом планировщика
        # Имя промпта совпадает с файлом в .ai/prompts/
        try:
            raw_plan = await self.runtime.execute_structured(
                prompt_name="DEVOS KERNEL PROMPT", 
                user_input=intent
            )
            
            # В будущем здесь будет парсинг реального ответа от LLM в ExecutionPlan
            return ExecutionPlan(
                intent=intent,
                tasks=[],
                risk_level="low",
                requires_confirmation=False
            )
        except Exception as e:
            from loguru import logger
            logger.error(f"Planning failed: {e}")
            raise

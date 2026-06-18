import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field

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
    Преобразует интент пользователя в структурированный граф задач.
    """
    
    def __init__(self, prompt_path: str = ".ai/prompts/DEVOS KERNEL PROMPT.md"):
        self.prompt_path = prompt_path

    def get_system_prompt(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    async def plan(self, intent: str) -> ExecutionPlan:
        # Здесь будет вызов AI Router для генерации плана на основе системного промпта.
        # Пока возвращаем пустой план-заглушку.
        return ExecutionPlan(
            intent=intent,
            tasks=[],
            risk_level="low",
            requires_confirmation=False
        )

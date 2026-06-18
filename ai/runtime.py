import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from loguru import logger
from pydantic import ValidationError

class AIRuntime:
    """
    Execution Layer (Motor).
    Отвечает за детерминированное выполнение запросов к LLM и валидацию JSON.
    """
    
    def __init__(self, cognitive_layer_path: str = ".ai"):
        self.cognitive_path = Path(cognitive_layer_path)

    def load_prompt(self, prompt_name: str) -> str:
        """Загружает когнитивную инструкцию из .ai/prompts/"""
        # Убираем расширение, если оно есть, для единообразия
        clean_name = prompt_name.replace(".md", "")
        prompt_file = self.cognitive_path / "prompts" / f"{clean_name}.md"
            
        if not prompt_file.exists():
            logger.error(f"Prompt {prompt_name} not found in {self.cognitive_path}")
            raise FileNotFoundError(f"Cognitive instruction {prompt_name} missing.")
            
        return prompt_file.read_text(encoding="utf-8")

    async def execute_structured(self, prompt_name: str, user_input: str) -> Dict[str, Any]:
        """
        Выполняет запрос и возвращает структурированный JSON.
        """
        system_prompt = self.load_prompt(prompt_name)
        logger.info(f"Executing AI task with prompt: {prompt_name}")
        
        # Здесь будет реальный вызов LLM через роутер провайдеров.
        # Для текущего этапа мы симулируем ответ, соответствующий новой спецификации.
        
        if prompt_name == "DEVOS KERNEL PROMPT":
            return self._mock_kernel_response(user_input)
            
        return {
            "status": "mock",
            "message": "AI Runtime is ready. Specific mock for this prompt not implemented."
        }

    def _mock_kernel_response(self, intent: str) -> Dict[str, Any]:
        """Симуляция ответа ИИ для планировщика."""
        return {
            "intent": intent,
            "graph": {
                "nodes": [
                    {"id": 1, "action": "fs.list", "input": {"path": "."}, "max_retries": 1},
                    {"id": 2, "action": "ai.analyze", "input": {"files": "$1.files"}, "max_retries": 0}
                ],
                "edges": [
                    [1, 2]
                ]
            },
            "risk_level": "low",
            "requires_confirmation": False
        }

    def validate_json(self, raw_text: str) -> Dict[str, Any]:
        """Парсинг и базовая валидация JSON из ответа LLM."""
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            raise

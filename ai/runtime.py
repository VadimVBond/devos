import json
from typing import Dict, Any, Optional
from pathlib import Path
from loguru import logger

class AIRuntime:
    """
    Execution Layer (Motor).
    Отвечает за детерминированное выполнение запросов к LLM.
    """
    
    def __init__(self, cognitive_layer_path: str = ".ai"):
        self.cognitive_path = Path(cognitive_layer_path)

    def load_prompt(self, prompt_name: str) -> str:
        """Загружает когнитивную инструкцию из .ai/prompts/"""
        prompt_file = self.cognitive_path / "prompts" / f"{prompt_name}.md"
        if not prompt_file.exists():
            # Попробуем без расширения .md, если передано полное имя
            prompt_file = self.cognitive_path / "prompts" / prompt_name
            
        if not prompt_file.exists():
            logger.error(f"Prompt {prompt_name} not found in {self.cognitive_path}")
            raise FileNotFoundError(f"Cognitive instruction {prompt_name} missing.")
            
        return prompt_file.read_text(encoding="utf-8")

    async def execute_structured(self, prompt_name: str, user_input: str) -> Dict[str, Any]:
        """
        Выполняет запрос и возвращает структурированный JSON.
        Здесь будет логика роутинга между провайдерами (OpenAI, Gemini и т.д.).
        """
        system_prompt = self.load_prompt(prompt_name)
        logger.info(f"Executing AI task with prompt: {prompt_name}")
        
        # Заглушка до реализации провайдеров
        return {
            "status": "mock",
            "message": "AI Runtime is ready. Providers not connected yet."
        }

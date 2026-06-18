import json
from pathlib import Path
from typing import List, Optional
from kernel.feedback.models import FeedbackPattern
from loguru import logger

class KnowledgeBase:
    """Вероятностное хранилище паттернов успешных и неудачных выполнений."""

    def __init__(self, db_path: str = ".runtime/knowledge/patterns.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.patterns: List[FeedbackPattern] = []
        self._load()

    def _load(self):
        if self.db_path.exists():
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.patterns = [FeedbackPattern(**p) for p in data]
            except Exception as e:
                logger.error(f"Failed to load Knowledge Base: {e}")
                self.patterns = []

    def _save(self):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump([p.model_dump() for p in self.patterns], f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save Knowledge Base: {e}")

    def add_pattern(self, pattern: FeedbackPattern):
        """Добавляет новый паттерн. Дедупликация может происходить на уровне FilterLayer, но базовую можно сделать тут."""
        self.patterns.append(pattern)
        self._save()

    def get_all_patterns(self) -> List[FeedbackPattern]:
        return self.patterns

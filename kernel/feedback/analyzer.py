from typing import Dict, Any, List
from loguru import logger
from kernel.feedback.models import FeedbackPattern
from kernel.feedback.knowledge_base import KnowledgeBase

class FeedbackAnalyzer:
    """Анализирует трейсы выполнения (или State) и генерирует уроки в базу знаний."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def analyze_execution_state(self, state: Dict[str, Any], graph_events: List[Dict[str, Any]] = None):
        """
        Extract patterns from execution results.
        If using Observability events, we parse TaskFailed events.
        """
        logger.info("Feedback Analyzer is scanning execution results...")
        
        if not graph_events:
            return

        for event in graph_events:
            if event.get("event_type") == "TaskFailed":
                action = event.get("action", "unknown")
                error = event.get("error", "Unknown error")
                
                # Create a pattern
                pattern = FeedbackPattern(
                    type="failure",
                    severity="high",  # Direct execution failure is high severity
                    source_task="GraphExecution",
                    action=action,
                    reason=f"Action '{action}' failed with error: {error}",
                    confidence=0.9
                )
                self.kb.add_pattern(pattern)
                logger.debug(f"Added new failure pattern for action {action}")
                
            elif event.get("event_type") == "TaskCompleted":
                # Optionally track successes if they are rare/complex
                pass

from typing import List, Dict, Any
from kernel.feedback.models import FeedbackPattern

class ContextBuilder:
    """Формирует финальный структурированный объект для передачи в AI Planner."""

    def build_context(self, filtered_patterns: List[FeedbackPattern]) -> Dict[str, Any]:
        if not filtered_patterns:
            return {}

        context_list = []
        for p in filtered_patterns:
            context_list.append({
                "pattern_id": p.pattern_id,
                "type": p.type,
                "severity": p.severity,
                "action": p.action,
                "reason": p.reason,
                "confidence": round(p.confidence, 2)
            })

        return {
            "feedback_context": context_list,
            "system_directive": "These are advisory patterns based on past executions. Use them to avoid known failures."
        }

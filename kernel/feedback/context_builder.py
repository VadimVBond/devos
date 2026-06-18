from typing import List, Dict, Any
from kernel.feedback.models import FeedbackPattern

class ContextBuilder:
    """Формирует финальный структурированный объект для передачи в AI Planner."""

    def build_context(self, filtered_patterns: List[FeedbackPattern]) -> Dict[str, Any]:
        if not filtered_patterns:
            return {}

        signals = []
        for p in filtered_patterns:
            signals.append({
                "type": p.type,
                "pattern_id": p.pattern_id,
                "severity": p.severity,
                "frequency": getattr(p, 'frequency', 1),
                "confidence": round(p.confidence, 2),
                "recommended_action": getattr(p, 'recommended_action', f"Avoid or fix action {p.action}")
            })

        return {
            "context_type": "feedback_signals",
            "signals": signals,
            "metadata": {
                "source": "knowledge_base",
                "filtered": True,
                "top_k": len(signals)
            }
        }

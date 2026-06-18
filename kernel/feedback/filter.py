from typing import List, Dict
from kernel.feedback.models import FeedbackPattern

class FilterLayer:
    """Фильтрует паттерны: удаляет дубликаты, ранжирует, оставляет Top-K."""

    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.severity_weight = {"high": 3, "medium": 2, "low": 1}

    def filter(self, patterns: List[FeedbackPattern]) -> List[FeedbackPattern]:
        # 1. Deduplication (by action + reason summary)
        unique_patterns: Dict[str, FeedbackPattern] = {}
        for p in patterns:
            # Create a logical key for deduplication
            # In a real system, we could use NLP embeddings. Here we use action + exact reason.
            key = f"{p.action}::{p.reason}"
            if key not in unique_patterns:
                unique_patterns[key] = p
            else:
                # Merge confidence or pick the latest
                existing = unique_patterns[key]
                existing.confidence = min(1.0, existing.confidence + 0.05)

        filtered_list = list(unique_patterns.values())

        # 2. Rank by severity and confidence
        filtered_list.sort(
            key=lambda p: (self.severity_weight.get(p.severity, 0) * p.confidence),
            reverse=True
        )

        # 3. Truncate to Top-K
        return filtered_list[:self.top_k]

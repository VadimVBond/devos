from typing import List, Tuple
from kernel.planner import ExecutionGraph
from kernel.optimizer.cost_model import CostModel

class BottleneckDetector:
    """Выявляет узкие места и опасные участки графа по стоимости."""

    def detect(self, graph: ExecutionGraph, batches: List[List[int]]) -> Tuple[List[str], str]:
        """
        Возвращает список сообщений об узких местах и общий уровень риска.
        """
        bottlenecks = []
        risk_level = "low"
        
        # Находим самый дорогой батч
        max_batch_cost = 0
        for i, batch in enumerate(batches):
            batch_cost = 0
            for node_id in batch:
                node = next((n for n in graph.nodes if n.id == node_id), None)
                if node:
                    batch_cost += CostModel.get_action_cost(node.action)
            
            if batch_cost > max_batch_cost:
                max_batch_cost = batch_cost
                
            # Если батч слишком тяжелый, это узкое место (Thundering Herd)
            if batch_cost > 100:
                bottlenecks.append(f"Batch {i} has high peak cost ({batch_cost}). Possible resource exhaustion.")
                risk_level = "medium"
                
        if max_batch_cost > 200:
            risk_level = "high"
            
        # Поиск длинных последовательных цепочек (глубина графа)
        if len(batches) > 10:
            bottlenecks.append(f"Graph is very deep ({len(batches)} layers). Execution might be slow.")
            
        return bottlenecks, risk_level

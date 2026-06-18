from typing import List, Tuple
from kernel.planner import ExecutionGraph

class ParallelAnalyzer:
    """Группирует узлы графа в детерминированные батчи на основе зависимостей (Topological Sort)."""

    def generate_batches(self, graph: ExecutionGraph) -> List[List[int]]:
        """
        Batch Stability Guarantee: 
        Один и тот же граф всегда порождает одни и те же батчи с одинаковым порядком узлов.
        """
        if not graph.nodes:
            return []

        # 1. Построение графа зависимостей
        in_degree = {n.id: 0 for n in graph.nodes}
        adj = {n.id: [] for n in graph.nodes}

        for src, dst in graph.edges:
            adj[src].append(dst)
            if dst in in_degree:
                in_degree[dst] += 1

        # 2. Послойный обход
        batches = []
        
        # Находим начальные узлы (in_degree == 0)
        # Сортируем для детерминизма
        current_layer = sorted([n for n, deg in in_degree.items() if deg == 0])

        while current_layer:
            batches.append(current_layer)
            next_layer = []
            
            for node_id in current_layer:
                for neighbor in adj.get(node_id, []):
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_layer.append(neighbor)
            
            # Сортировка для гарантии стабильности внутри батча (детерминизм)
            current_layer = sorted(next_layer)

        return batches

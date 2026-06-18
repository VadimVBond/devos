import copy
from typing import List
from kernel.planner import ExecutionGraph

class GraphRewriter:
    """Безопасно модифицирует граф, удаляя дубликаты и неэффективные пути."""

    def simplify(self, graph: ExecutionGraph, changes_log: List[str]) -> ExecutionGraph:
        """
        Удаляет узлы-дубликаты (одинаковый action и input).
        """
        new_graph = copy.deepcopy(graph)
        
        unique_nodes = {}
        duplicates = {}
        
        for node in new_graph.nodes:
            # Сериализуем action и input для сравнения
            # В реальной системе нужно быть осторожнее со словарями (сортировать ключи)
            key = f"{node.action}::{repr(sorted(node.input.items()))}"
            if key in unique_nodes:
                duplicates[node.id] = unique_nodes[key]
            else:
                unique_nodes[key] = node.id

        if duplicates:
            # Удаляем дублирующиеся узлы
            new_graph.nodes = [n for n in new_graph.nodes if n.id not in duplicates]
            
            # Перенаправляем ребра
            new_edges = []
            for src, dst in new_graph.edges:
                new_src = duplicates.get(src, src)
                new_dst = duplicates.get(dst, dst)
                if new_src != new_dst and (new_src, new_dst) not in new_edges:
                    new_edges.append((new_src, new_dst))
                    
            new_graph.edges = new_edges
            
            for dup_id, orig_id in duplicates.items():
                changes_log.append(f"Merged duplicate node {dup_id} into {orig_id}.")
                
        return new_graph

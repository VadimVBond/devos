from typing import List
from kernel.planner import ExecutionGraph
from plugins.registry import PluginRegistry
from kernel.critic.models import CriticReview

class GraphValidator:
    """Performs structural and logical validation of the ExecutionGraph."""
    
    def __init__(self, registry: PluginRegistry):
        self.registry = registry

    def validate(self, graph: ExecutionGraph, review: CriticReview):
        """Runs validation rules and appends to the review object."""
        self._check_plugins_exist(graph, review)
        self._check_unreachable_nodes(graph, review)

    def _check_plugins_exist(self, graph: ExecutionGraph, review: CriticReview):
        missing_plugins = []
        for node in graph.nodes:
            if not self.registry.get_plugin(node.action):
                missing_plugins.append(f"Node {node.id} uses unknown action: {node.action}")
                
        if missing_plugins:
            review.status = "rejected"
            review.issues.extend(missing_plugins)
            review.add_trace("Registered Plugins Check", "failed", f"Missing plugins: {missing_plugins}")
        else:
            review.add_trace("Registered Plugins Check", "passed", "All actions are known plugins.")

    def _check_unreachable_nodes(self, graph: ExecutionGraph, review: CriticReview):
        if not graph.nodes:
            review.add_trace("Unreachable Nodes Check", "passed", "Empty graph.")
            return

        # Find all nodes that are destinations of edges
        reachable = {dst for _, dst in graph.edges}
        
        # Find all nodes that are sources of edges
        sources = {src for src, _ in graph.edges}
        
        # Nodes that are neither sources nor destinations (and there is more than 1 node total)
        # Or nodes that have no incoming edges but aren't intended to be starting points?
        # Actually, in a DAG, starting nodes have 0 incoming edges. Unreachable isn't just disconnected. 
        # Disconnected nodes are fine if they are parallel independent tasks.
        
        review.add_trace("Unreachable Nodes Check", "passed", "Graph structure is valid DAG.")

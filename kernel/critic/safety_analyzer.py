from kernel.planner import ExecutionGraph
from kernel.critic.models import CriticReview

class SafetyAnalyzer:
    """Analyzes the graph for destructive or risky operations."""

    DANGEROUS_ACTIONS = ["fs.rm", "fs.delete", "git.reset", "git.push_force"]
    
    def analyze(self, graph: ExecutionGraph, review: CriticReview):
        self._check_destructive_actions(graph, review)

    def _check_destructive_actions(self, graph: ExecutionGraph, review: CriticReview):
        risky_nodes = []
        for node in graph.nodes:
            if node.action in self.DANGEROUS_ACTIONS:
                risky_nodes.append(f"Node {node.id} uses dangerous action: {node.action}")
            
            # Simple heuristic for destructive shell commands if we had a shell plugin
            if node.action == "system.shell" and "rm -rf" in str(node.input):
                risky_nodes.append(f"Node {node.id} contains 'rm -rf' in shell command.")
                
        if risky_nodes:
            review.status = "rejected"
            review.issues.extend(risky_nodes)
            review.add_trace("Safety Rules Check", "failed", f"Destructive operations detected: {risky_nodes}")
        else:
            review.add_trace("Safety Rules Check", "passed", "No strictly dangerous actions found.")

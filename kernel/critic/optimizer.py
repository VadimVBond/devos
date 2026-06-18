import copy
from kernel.planner import ExecutionGraph
from kernel.critic.models import CriticReview

class GraphOptimizer:
    """Proposes modifications to optimize the graph without mutating the original in-place."""

    def optimize(self, original_graph: ExecutionGraph, review: CriticReview):
        # We only try to optimize if it's currently approved. No point optimizing a rejected graph.
        if review.status == "rejected":
            review.add_trace("Optimization", "passed", "Skipped optimization due to rejected status.")
            return

        final_graph = copy.deepcopy(original_graph)
        optimizations_found = []

        # Example Heuristic: Merge exact duplicate nodes
        # If two nodes have the exact same action and inputs, we can keep the first and remap edges
        unique_tasks = {}
        duplicates = {}
        for node in final_graph.nodes:
            # We serialize action and input to use as a dictionary key
            key = f"{node.action}:{str(node.input)}"
            if key in unique_tasks:
                duplicates[node.id] = unique_tasks[key]
            else:
                unique_tasks[key] = node.id

        if duplicates:
            # Filter out duplicate nodes
            final_graph.nodes = [n for n in final_graph.nodes if n.id not in duplicates]
            
            # Remap edges
            new_edges = []
            for src, dst in final_graph.edges:
                new_src = duplicates.get(src, src)
                new_dst = duplicates.get(dst, dst)
                if new_src != new_dst and (new_src, new_dst) not in new_edges:
                    new_edges.append((new_src, new_dst))
            final_graph.edges = new_edges
            
            for dup_id, orig_id in duplicates.items():
                optimizations_found.append(f"Merged duplicate node {dup_id} into {orig_id}.")
                
        if optimizations_found:
            review.status = "modified"
            review.optimizations.extend(optimizations_found)
            review.final_graph = final_graph
            review.add_trace("Graph Optimizer", "passed", f"Applied optimizations: {optimizations_found}")
        else:
            review.add_trace("Graph Optimizer", "passed", "No structural optimizations found.")

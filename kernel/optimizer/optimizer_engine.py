from loguru import logger
from kernel.planner import ExecutionGraph
from kernel.optimizer.models import OptimizedExecutionGraph
from kernel.optimizer.cost_model import CostModel
from kernel.optimizer.parallel_analyzer import ParallelAnalyzer
from kernel.optimizer.graph_rewriter import GraphRewriter
from kernel.optimizer.bottleneck_detector import BottleneckDetector

class OptimizerEngine:
    """
    Главный движок оптимизатора.
    Получает граф от CriticEngine и возвращает OptimizedExecutionGraph.
    """
    
    def __init__(self):
        self.rewriter = GraphRewriter()
        self.analyzer = ParallelAnalyzer()
        self.detector = BottleneckDetector()
        logger.info("Execution Optimizer initialized.")

    def optimize(self, graph: ExecutionGraph) -> OptimizedExecutionGraph:
        """
        Производит безопасную трансформацию и пакетирование графа.
        """
        logger.info("Starting execution optimization...")
        changes_log = []
        
        # 1. Simplification (safe duplicate removal)
        optimized_graph = self.rewriter.simplify(graph, changes_log)
        
        # 2. Batching (Topological parallel grouping)
        batches = self.analyzer.generate_batches(optimized_graph)
        
        # 3. Cost Analysis
        cost_analysis = self._analyze_cost(optimized_graph, batches)
        
        # 4. Bottleneck Detection
        bottlenecks, risk = self.detector.detect(optimized_graph, batches)
        
        result = OptimizedExecutionGraph(
            original_graph=graph,
            optimized_graph=optimized_graph,
            execution_batches=batches,
            cost_analysis=cost_analysis,
            performance_score=self._calculate_score(cost_analysis, batches),
            changes_log=changes_log,
            bottlenecks=bottlenecks,
            execution_risk=risk
        )
        
        logger.success(f"Graph optimized into {len(batches)} batches.")
        return result

    def _analyze_cost(self, graph: ExecutionGraph, batches: list) -> dict:
        total_cost = 0
        for node in graph.nodes:
            total_cost += CostModel.get_action_cost(node.action)
        return {"total_cost": total_cost, "batch_count": len(batches)}

    def _calculate_score(self, cost_analysis: dict, batches: list) -> float:
        # Simple heuristic: lower depth and lower cost = better score
        # Base score 1.0, minus penalty for depth
        depth = len(batches)
        if depth == 0: return 1.0
        return max(0.1, 1.0 - (depth * 0.05))

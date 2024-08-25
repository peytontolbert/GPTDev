# agents/strategy_evaluation_agent.py

from agents.base_agent import Agent
import json
from typing import Dict, Any, List

class StrategyEvaluationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, strategy: Dict[str, Any]) -> float:
        score = 0
        if "efficiency" in strategy:
            score += strategy["efficiency"] * 0.4  # Weight for efficiency
        if "feasibility" in strategy:
            score += strategy["feasibility"] * 0.3  # Weight for feasibility
        if "impact" in strategy:
            score += strategy["impact"] * 0.3  # Weight for impact

        return score

    def select_best_strategy(self, strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        best_strategy = None
        highest_score = -1

        for strategy in strategies:
            score = self.execute(strategy)
            if score > highest_score:
                highest_score = score
                best_strategy = strategy

        return best_strategy

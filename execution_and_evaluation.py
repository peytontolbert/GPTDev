import importlib
from typing import List, Dict, Any
import os
class ExecutionAndEvaluation:
    def __init__(self, directory, inter_agent_communication_agent, agent_improvement_agent, testing_agent, performance_evaluation_agent, meta_learning_agent):
        self.directory = directory
        self.inter_agent_communication_agent = inter_agent_communication_agent
        self.agent_improvement_agent = agent_improvement_agent
        self.testing_agent = testing_agent
        self.performance_evaluation_agent = performance_evaluation_agent
        self.meta_learning_agent = meta_learning_agent
        self.performance_metrics: Dict[str, float] = {}

    def run_selected_agents(self, agents: List[str], requirements: Dict[str, Any]) -> List[Any]:
        results = []
        for agent in agents:
            agent_module = importlib.import_module(f'agents.{agent[:-3]}')  # Remove '.py'
            agent_instance = getattr(agent_module, 'AgentClass')()
            result = agent_instance.execute(requirements)
            results.append(result)
            # Pass the result to Inter-Agent Communication Agent
            self.inter_agent_communication_agent.share_result(agent, result)
            # Handle test results and updates...
            # Run tests and handle any failures using TestingAgent
            agent_code = self.agent_improvement_agent.load_agent_code(f"{agent}.py")
            fixed_code = self.testing_agent.execute(agent, agent_code)
            if fixed_code and fixed_code != agent_code:
                self.save_agent_code(f"{agent}.py", fixed_code)
                self.agent_improvement_agent.version_control.add_version(agent, fixed_code, "Test failure fixes")
        
        return results

    def evaluate_and_improve(self, agents: List[str], results: List[Any], original_input) -> None:
        for agent, result in zip(agents, results):
            input_data = {"agent_name": agent, "result": result, "original_input": original_input}
            performance_score = self.performance_evaluation_agent.execute(input_data)
            self.performance_metrics[agent] = performance_score
            print(performance_score)
            if performance_score < 0.7:  # Threshold for improvement
                self.agent_improvement_agent.improve_agent(agent)
        
        # Use meta-learning agent to refine improvement strategies
        meta_analysis = self.meta_learning_agent.execute(self.performance_metrics)
        self.meta_learning_agent.adjust_improvement_strategies(meta_analysis, self.agent_improvement_agent.agent_details)

    def save_agent_code(self, filename: str, code: str) -> None:
        with open(os.path.join(self.directory, filename), 'w') as f:
            f.write(code)


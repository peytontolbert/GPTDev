import openai
import os
import json
import importlib

from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
from typing import List, Dict, Any

from agent_version_control import AgentVersionControl
from agent_initialization import AgentInitialization
from optimization_and_generalization import OptimizationAndGeneralization
from execution_and_evaluation import ExecutionAndEvaluation
from utility_functions import UtilityFunctions

class BuilderGPT(Agent):
    def __init__(self, name, prompt, directory):
        super().__init__(name)
        self.prompt = prompt
        self.directory = directory
        self.gpt = ChatGPT()
        self.agent_details = {}
        self.version_control = AgentVersionControl()
        self.performance_metrics: Dict[str, float] = {}
        self.docker_client = None

        # Initialize Agents
        self.agent_initialization = AgentInitialization(name, prompt, directory, self.version_control, self.agent_details)
        self.optimization_and_generalization = OptimizationAndGeneralization(directory, self.gpt, self.version_control)
        self.execution_and_evaluation = ExecutionAndEvaluation(directory, self.agent_initialization.inter_agent_communication_agent, self.agent_initialization.agent_improvement_agent, self.agent_initialization.testing_agent, self.agent_initialization.performance_evaluation_agent, self.agent_initialization.meta_learning_agent)

    def optimize_agent(self, agent_name, optimization_details):
        self.optimization_and_generalization.optimize_agent(agent_name, optimization_details)

    def generalize_agent(self, agent_name, generalization_details):
        return self.optimization_and_generalization.generalize_agent(agent_name, generalization_details)

    def run_selected_agents(self, agents: List[str], requirements: Dict[str, Any]) -> List[Any]:
        return self.execution_and_evaluation.run_selected_agents(agents, requirements)

    def evaluate_and_improve(self, agents: List[str], results: List[Any], original_input) -> None:
        self.execution_and_evaluation.evaluate_and_improve(agents, results, original_input)

    def save_agent_code(self, filename: str, code: str) -> None:
        UtilityFunctions.save_to_file(os.path.join(self.directory, filename), code)


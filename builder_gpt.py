import openai
import os
import json
import importlib
from agents.task_decomposition_agent import TaskDecompositionAgent  # Import the new agent
from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent  # Import the new agent
from agents.code_review_agent import CodeReviewAgent  # Import the new agent
from agents.meta_learning_agent import MetaLearningAgent  # Import the new agent
from agents.exploration_strategy_agent import ExplorationStrategyAgent  # Import the new agent
from agents.performance_evaluation_agent import PerformanceEvaluationAgent  # Import the new agent
from agents.agent_improvement_agent import AgentImprovementAgent  # Import the new agent
from agents.testing_agent import TestingAgent  # Import the new agent
from agents.deployment_agent import DeploymentAgent  # Import the new agent
from agents.strategy_evaluation_agent import StrategyEvaluationAgent  # Import the new agent
from agents.agent_update_manager_agent import AgentUpdateManager # Import the new agent
from agents.dependency_management_agent import DependencyManagementAgent # Import the new agent
from agents.task_manager_agent import TaskManagerAgent # Import the new agent

from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
from datetime import datetime
from typing import List, Dict, Any, Union, Tuple
import unittest
import git
import docker

class AgentVersion:
    def __init__(self, code, version=1, changes="Initial version"):
        self.code = code
        self.version = version
        self.changes = changes
        self.timestamp = datetime.now().isoformat()

class AgentVersionControl:
    def __init__(self):
        self.versions = {}

    def add_version(self, agent_name, code, changes):
        if agent_name not in self.versions:
            self.versions[agent_name] = []
        new_version = len(self.versions[agent_name]) + 1
        self.versions[agent_name].append(AgentVersion(code, new_version, changes))
        return new_version

    def get_latest_version(self, agent_name):
        return self.versions[agent_name][-1] if agent_name in self.versions else None

    def rollback(self, agent_name, version):
        if agent_name in self.versions and 1 <= version <= len(self.versions[agent_name]):
            return self.versions[agent_name][version - 1].code
        return None

    def get_changelog(self, agent_name):
        if agent_name not in self.versions:
            return ""
        changelog = f"# Changelog for {agent_name}\n\n"
        for version in reversed(self.versions[agent_name]):
            changelog += f"## Version {version.version} - {version.timestamp}\n"
            changelog += f"{version.changes}\n\n"
        return changelog

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
        self.git_repo = git.Repo(self.directory)

        #Initialize Agents 
        self.task_decomposition_agent = TaskDecompositionAgent(name="TaskDecompositionAgent")  # Instantiate the agent
        self.knowledge_retrieval_agent = KnowledgeRetrievalAgent(name="KnowledgeRetrievalAgent")  # Instantiate the agent
        self.code_review_agent = CodeReviewAgent(name="CodeReviewAgent")  # Instantiate the agent
        self.meta_learning_agent = MetaLearningAgent(name="MetaLearningAgent")  # Instantiate the agent
        self.exploration_strategy_agent = ExplorationStrategyAgent(name="ExplorationStrategyAgent")  # Instantiate the agent
        self.performance_evaluation_agent = PerformanceEvaluationAgent(name="PerformanceEvaluationAgent", prompt=self.prompt)
        self.testing_agent = TestingAgent(name="TestingAgent")
        self.deployment_agent = DeploymentAgent(name="DeploymentAgent", directory=directory)
        self.strategy_evaluation_agent = StrategyEvaluationAgent(name="StrategyEvaluationAgent")
        self.agent_update_manager = AgentUpdateManager(name="AgentUpdateManager", directory=directory, version_control=self.version_control)
        self.dependency_manager_agent = DependencyManagementAgent(name="DependencyManagerAgent")
        self.agent_improvement_agent = AgentImprovementAgent(self.knowledge_retrieval_agent, self.dependency_manager_agent, self.agent_update_manager, self.directory, self.version_control)

        # Task Manager Agent
        self.task_manager_agent = TaskManagerAgent(name="TaskManagerAgent", agents={
            'task_decomposition': self.task_decomposition_agent,
            'knowledge_retrieval': self.knowledge_retrieval_agent,
            'code_review': self.code_review_agent,
            'meta_learning': self.meta_learning_agent,
            'exploration_strategy': self.exploration_strategy_agent,
            'performance_evaluation': self.performance_evaluation_agent,
            'agent_improvement': self.agent_improvement_agent,
            'testing': self.testing_agent,
            'deployment': self.deployment_agent,
            'strategy_evaluation': self.strategy_evaluation_agent,
            'dependency_manager': self.dependency_manager_agent,
            'agent_update_manager': self.agent_update_manager
        })

        # Initialize Docker client if Docker is available
        try:
            self.docker_client = docker.from_env()
            print("Docker client initialized successfully.")
        except docker.errors.DockerException as e:
            print(f"Warning: Docker could not be initialized. Error: {e}")
            self.docker_client = None

    def execute(self, input_data):
        tasks = ['task_decomposition', 'knowledge_retrieval', 'code_review', 'meta_learning', 'exploration_strategy']
        results = self.task_manager_agent.execute_tasks(tasks, input_data)
        self.evaluate_and_improve(results.keys(), results.values())

        for agent in results.keys():
            self.deployment_agent.execute(agent)
        return results

    
    def implement_optimization(self, agent_name, optimization_suggestions):
        new_agents = []
        try:
            # Ensure optimization_suggestions is a list of dictionaries
            if isinstance(optimization_suggestions, str):
                optimization_suggestions = json.loads(optimization_suggestions)
            
            if not isinstance(optimization_suggestions, list) or not all(isinstance(suggestion, dict) for suggestion in optimization_suggestions):
                raise ValueError("Optimization suggestions are not in the expected format.")

            for suggestion in optimization_suggestions:
                if suggestion.get('type') == 'decomposition':
                    new_agents.extend(self.decompose_agent(agent_name, suggestion['details']))
                elif suggestion.get('type') == 'optimization':
                    self.optimize_agent(agent_name, suggestion['details'])
                elif suggestion.get('type') == 'generalization':
                    new_agents.append(self.generalize_agent(agent_name, suggestion['details']))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error processing optimization suggestions: {e}")
        
        return new_agents

    def optimize_agent(self, agent_name, optimization_details):
        agent_file = f"{agent_name}.py"
        with open(os.path.join(self.directory, agent_file), 'r') as f:
            original_code = f.read()
        
        optimization_prompt = f"Optimize the following agent code based on these details:\n{optimization_details}\n\nOriginal code:\n{original_code}"
        optimized_code = self.gpt.chat_with_ollama(optimization_prompt, self.prompt)
        
        self.save_to_file(os.path.join(self.directory, agent_file), optimized_code)
        
        # Add new version
        changes = f"Optimized agent based on: {optimization_details}"
        new_version = self.version_control.add_version(agent_name, optimized_code, changes)
        
        # Update CHANGELOG.md
        changelog = self.version_control.get_changelog(agent_name)
        self.save_to_file(os.path.join(self.directory, f'{agent_name}_CHANGELOG.md'), changelog)

    def generalize_agent(self, agent_name, generalization_details):
        agent_file = f"{agent_name}.py"
        with open(os.path.join(self.directory, agent_file), 'r') as f:
            original_code = f.read()
        
        generalization_prompt = f"Generalize the following agent code based on these details:\n{generalization_details}\n\nOriginal code:\n{original_code}"
        generalized_code = self.gpt.chat_with_ollama(generalization_prompt, self.prompt)
        
        new_agent_name = f"{generalization_details['new_name']}_agent.py"
        self.save_to_file(os.path.join(self.directory, new_agent_name), generalized_code)
        
        # Add new version
        changes = f"Created generalized agent {generalization_details['new_name']} from {agent_name}"
        self.version_control.add_version(generalization_details['new_name'], generalized_code, changes)
        
        return new_agent_name

    def run_selected_agents(self, agents: List[str], requirements: Dict[str, Any]) -> List[Any]:
        results = []
        for agent in agents:
            agent_module = importlib.import_module(f'agents.{agent[:-3]}')  # Remove '.py'
            agent_instance = getattr(agent_module, 'AgentClass')()
            result = agent_instance.execute(requirements)
            results.append(result)
            # Run tests and handle any failures using TestingAgent
            agent_code = self.agent_improvement_agent.load_agent_code(f"{agent}.py")
            fixed_code = self.testing_agent.execute(agent, agent_code)
            if fixed_code and fixed_code != agent_code:
                self.save_agent_code(f"{agent}.py", fixed_code)
                self.version_control.add_version(agent, fixed_code, "Test failure fixes")
        
        return results

    def evaluate_and_improve(self, agents: List[str], results: List[Any]) -> None:
        for agent, result in zip(agents, results):
            performance_score = self.performance_evaluation_agent.evaluate_performance(agent, result)
            self.performance_metrics[agent] = performance_score

            if performance_score < 0.7:  # Threshold for improvement
                self.agent_improvement_agent.improve_agent(agent)
        
        # Use meta-learning agent to refine improvement strategies
        meta_analysis = self.meta_learning_agent.execute(self.performance_metrics)
        self.meta_learning_agent.adjust_improvement_strategies(meta_analysis, self.agent_details)

    def save_agent_code(self, filename: str, code: str) -> None:
        Agent.save_to_file(os.path.join(self.directory, filename), code)
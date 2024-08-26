import os
import zipfile
import importlib
from agents.base_agent import Agent

class AgentSearchAgent(Agent):
    def __init__(self, name="AgentSearchAgent", directory="agents"):
        super().__init__(name)
        self.directory = directory

    def execute(self, agent):
        agent = self.search_agents(agent)
        return agent

    def perform_task(self, search_criteria):
        """
        Searches for agents that match the given criteria.
        :param search_criteria: A string or dictionary defining the search criteria (e.g., agent name, function name).
        :return: A list of agent names and their paths that match the criteria.
        """
        agents = self.search_agents(search_criteria)
        return agents

    def search_agents(self, search_criteria):
        """
        Search for agents in the directory that match the search criteria.
        :param search_criteria: The criteria to search for.
        :return: A list of agent names and their details.
        """
        matched_agents = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('_agent.py'):
                    agent_name = file[:-3]  # Remove .py extension
                    if search_criteria.lower() in agent_name.lower():
                        matched_agents.append({
                            "agent_name": agent_name,
                            "path": os.path.join(root, file)
                        })
        return matched_agents

    def import_agent(self, agent_name):
        """
        Dynamically imports an agent by its name.
        :param agent_name: The name of the agent to import.
        :return: The imported agent module.
        """
        try:
            module = importlib.import_module(f'agents.{agent_name}')
            return module
        except ImportError as e:
            return f"Error importing {agent_name}: {str(e)}"

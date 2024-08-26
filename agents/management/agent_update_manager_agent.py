# agents/agent_update_manager.py

from agents.base_agent import Agent
import os

class AgentUpdateManager(Agent):
    def __init__(self, name, directory, version_control):
        super().__init__(name)
        self.directory = directory
        self.version_control = version_control

    def execute():
        pass

    def update_agent(self, agent_name: str, updated_code: str, changes: str):
        file_path = os.path.join(self.directory, f"{agent_name}.py")
        self.save_to_file(agent_name, updated_code)
        self.version_control.add_version(agent_name, updated_code, changes)
        changelog = self.version_control.get_changelog(agent_name)
        self.save_to_file(os.path.join(self.directory, f'{agent_name}_CHANGELOG.md'), changelog)

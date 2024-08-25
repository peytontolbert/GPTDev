from agents.base_agent import Agent
import subprocess
import os

class DependencyManagementAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.dependencies = {}

    def perform_task(self, input_data):
        dependencies = self.parse_dependencies(input_data)
        self.install_dependencies(dependencies)

    def parse_dependencies(self, input_data):
        # Implement logic to parse dependencies from input_data
        return input_data.split('\n')

    def install_dependencies(self, dependencies):
        for dependency in dependencies:
            subprocess.run(['pip', 'install', dependency])


    def add_dependency(self, agent, depends_on):
        if agent not in self.dependencies:
            self.dependencies[agent] = set()
        self.dependencies[agent].add(depends_on)

    def remove_agent(self, agent):
        self.dependencies.pop(agent, None)
        for deps in self.dependencies.values():
            deps.discard(agent)

    def get_dependencies(self, agent):
        return self.dependencies.get(agent, set())

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for agent, deps in self.dependencies.items():
                f.write(f"{agent}: {', '.join(deps)}\n")
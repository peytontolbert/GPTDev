import openai
import os
import json
import importlib
from base_agent import Agent
from chat.chat_with_ollama import ChatGPT
from datetime import datetime

class AgentDependencyGraph:
    def __init__(self):
        self.dependencies = {}

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
        self.dependency_graph = AgentDependencyGraph()
        self.version_control = AgentVersionControl()

    def execute(self, input_data):
        optimized_agents = self.recursive_agent_optimization(os.listdir(self.directory))
        selected_agents = self.dynamic_selection(optimized_agents)
        results = self.run_selected_agents(selected_agents, input_data)
        return results

    def recursive_agent_optimization(self, agent_list, depth=0, max_depth=3):
        if depth >= max_depth:
            return agent_list

        optimized_agents = []
        for agent in agent_list:
            if agent.endswith('_agent.py'):
                agent_name = agent[:-3]  # Remove '.py'
                agent_details, dependencies = self.get_agent_details(agent_name)
                optimization_suggestions = self.analyze_and_optimize_agent(agent_name, agent_details)
                new_agents = self.implement_optimization(agent_name, optimization_suggestions)
                optimized_agents.extend(new_agents)
                
                # Update dependencies
                for dep in dependencies:
                    self.dependency_graph.add_dependency(agent_name, dep)
                
                # Recursively optimize new agents
                sub_optimized = self.recursive_agent_optimization(new_agents, depth + 1, max_depth)
                optimized_agents.extend(sub_optimized)
            else:
                optimized_agents.append(agent)

        self.dependency_graph.save_to_file(os.path.join(self.directory, 'dependencies.md'))
        return list(set(optimized_agents))  # Remove duplicates

    def get_agent_details(self, agent_name):
        if agent_name not in self.agent_details:
            agent_file = f"{agent_name}.py"
            with open(os.path.join(self.directory, agent_file), 'r') as f:
                agent_code = f.read()
            
            details_prompt = (
                f"Analyze the following agent code and provide:\n"
                f"1. A brief summary of its functionality and key methods\n"
                f"2. A list of other agents or modules it depends on\n\n{agent_code}"
            )
            response = self.gpt.chat_with_ollama(details_prompt, self.prompt)
            parsed_response = self.parse_response(response)
            self.agent_details[agent_name] = parsed_response['summary']
            dependencies = parsed_response.get('dependencies', [])

        return self.agent_details[agent_name], dependencies

    def analyze_and_optimize_agent(self, agent_name, agent_details):
        optimization_prompt = (
            f"Given the following agent details:\n{agent_details}\n\n"
            "Suggest optimizations or decompositions for this agent. Consider:\n"
            "1. Can it be split into smaller, more focused agents?\n"
            "2. Are there any redundant functionalities that can be removed or combined?\n"
            "3. Can any of its functions be generalized for broader use?\n"
            "Provide specific recommendations in a structured format."
        )
        optimization_suggestions = self.gpt.chat_with_ollama(optimization_prompt, self.prompt)
        return self.parse_response(optimization_suggestions)

    def implement_optimization(self, agent_name, optimization_suggestions):
        new_agents = []
        for suggestion in optimization_suggestions:
            if suggestion['type'] == 'decomposition':
                new_agents.extend(self.decompose_agent(agent_name, suggestion['details']))
            elif suggestion['type'] == 'optimization':
                self.optimize_agent(agent_name, suggestion['details'])
            elif suggestion['type'] == 'generalization':
                new_agents.append(self.generalize_agent(agent_name, suggestion['details']))
        return new_agents

    def decompose_agent(self, agent_name, decomposition_details):
        new_agent_names = []
        for new_agent in decomposition_details['new_agents']:
            new_agent_name = f"{new_agent['name']}_agent.py"
            new_agent_code = self.generate_agent_code(new_agent['name'], new_agent['functionality'])
            self.save_to_file(os.path.join(self.directory, new_agent_name), new_agent_code)
            new_agent_names.append(new_agent_name)
            
            # Add new version
            changes = f"Created new agent {new_agent['name']} from decomposition of {agent_name}"
            self.version_control.add_version(new_agent['name'], new_agent_code, changes)
        
        # Update the original agent to use the new decomposed agents
        self.update_agent_to_use_decomposed(agent_name, decomposition_details['new_agents'])
        
        return new_agent_names

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

    def generate_agent_code(self, agent_name, functionality):
        code_generation_prompt = f"Generate a Python agent class named {agent_name} with the following functionality:\n{functionality}"
        generated_code = self.gpt.chat_with_ollama(code_generation_prompt, self.prompt)
        return generated_code

    def update_agent_to_use_decomposed(self, original_agent_name, new_agents):
        agent_file = f"{original_agent_name}.py"
        with open(os.path.join(self.directory, agent_file), 'r') as f:
            original_code = f.read()
        
        update_prompt = (
            f"Update the following agent code to use these new decomposed agents:\n{new_agents}\n\n"
            f"Original code:\n{original_code}\n\n"
            "Ensure the original agent now coordinates these new agents instead of performing the tasks directly."
        )
        updated_code = self.gpt.chat_with_ollama(update_prompt, self.prompt)
        self.save_to_file(os.path.join(self.directory, agent_file), updated_code)
        
        # Add new version
        changes = f"Updated to use new decomposed agents: {', '.join([agent['name'] for agent in new_agents])}"
        new_version = self.version_control.add_version(original_agent_name, updated_code, changes)
        
        # Update CHANGELOG.md
        changelog = self.version_control.get_changelog(original_agent_name)
        self.save_to_file(os.path.join(self.directory, f'{original_agent_name}_CHANGELOG.md'), changelog)

    def dynamic_selection(self, agent_list):
        selection_prompt = (
            f"Given the following list of agents:\n{agent_list}\n\n"
            "Select the most appropriate agents for the current task. "
            "Consider the agents' functionalities and how they can work together effectively."
        )
        selected_agents = self.gpt.chat_with_ollama(selection_prompt, self.prompt)
        return self.parse_response(selected_agents)

    def run_selected_agents(self, agents, input_data):
        results = []
        for agent in agents:
            agent_module = importlib.import_module(f'agents.{agent[:-3]}')  # Remove '.py'
            agent_instance = getattr(agent_module, 'AgentClass')()
            result = agent_instance.execute(input_data)
            results.append(result)
        return results

    def parse_response(self, response):
        if isinstance(response, str):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"raw_response": response}
        elif isinstance(response, (dict, list)):
            return response
        else:
            print("Unexpected data type received.")
            return None
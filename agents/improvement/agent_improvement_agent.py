# agents/agent_improvement_agent.py

from agents.base_agent import Agent
import json
import os

"""
    OLD ANALYZE AND OPTIMIZE FUNCTION
    def analyze_and_optimize_agent(self, agent_name, agent_details):
        # Retrieve external knowledge
        external_knowledge = self.knowledge_retrieval_agent.execute(agent_details)
        strategies = self.exploration_strategy_agent.execute(agent_details)
        best_strategy = self.strategy_evaluation_agent.select_best_strategy(strategies)
        optimization_prompt = (
            f"Given the following agent details and external knowledge:\n{agent_details}\n{external_knowledge}\n\n"
            f"Implement the best strategy from the following:\n{best_strategy}\n"
            "Provide specific recommendations in a structured format."
        )
        optimization_suggestions = self.gpt.chat_with_ollama(optimization_prompt, self.prompt)
        return self.parse_response(optimization_suggestions)
"""
class AgentImprovementAgent(Agent):
    def __init__(self, name, knowledge_retrieval_agent, dependency_manager_agent, agent_update_manager, directory, version_control):
        super().__init__(name)
        self.knowledge_retrieval_agent = knowledge_retrieval_agent
        self.dependency_manager_agent = dependency_manager_agent
        self.directory = directory
        self.agent_update_manager = agent_update_manager
        self.version_control = version_control

    def execute(self, input_data):
        agent_name = input_data['agent_name']
        agent_code =input_data['agent_code']
        system_prompt = self.generate_prompt()
        improvement_prompt = (
            f"The following agent has underperformed:\n{agent_name}\n\n"
            f"Current implementation:\n{agent_code}\n\n"
            "Suggest improvements to enhance its performance."
        )
        improved_code = self.gpt.chat_with_ollama(system_prompt, improvement_prompt)
        return improved_code

    def generate_prompt(self):
        return "You are an Autonomous Agent Improver. Respond in a structured JSON format"
    
    def recursive_agent_optimization(self, agent_list, depth=0, max_depth=3):
        if depth >= max_depth:
            return agent_list

        optimized_agents = []
        for agent in agent_list:
            if agent.endswith('_agent.py'):
                agent_name = agent[:-3]  # Remove '.py'
                agent_details, dependencies = self.knowledge_retrieval_agent.get_agent_details(self.directory, agent_name, agent_details, self.prompt)
                optimization_suggestions = self.analyze_and_optimize_agent(agent_name, agent_details)
                new_agents = self.implement_optimization(agent_name, optimization_suggestions)
                optimized_agents.extend(new_agents)
                
                # Update dependencies
                for dep in dependencies:
                    self.dependency_manager_agent.add_dependency(agent_name, dep)
                
                # Recursively optimize new agents
                sub_optimized = self.recursive_agent_optimization(new_agents, depth + 1, max_depth)
                optimized_agents.extend(sub_optimized)
            else:
                optimized_agents.append(agent)

        self.dependency_graph.save_to_file(os.path.join(self.directory, 'dependencies.md'))
        return list(set(optimized_agents))  # Remove duplicates

    def analyze_and_optimize_agent(self, agent_name, agent_details):
        # Placeholder function to analyze and suggest optimizations
        # This function can be extended or replaced with more complex logic
        optimization_prompt = (
            f"Given the following agent details:\n{json.dumps(agent_details, indent=2)}\n\n"
            "Suggest possible optimizations or improvements."
        )
        optimization_suggestions = self.gpt.chat_with_ollama(self.generate_prompt(), optimization_prompt)
        return json.loads(optimization_suggestions)
    def implement_optimization(self, agent_name, optimization_suggestions):
        new_agents = []
        try:
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
    
    def improve_agent(self, agent: str) -> None:
        agent_code = self.load_agent_code(f"{agent}.py")
        input_data = {"agent": agent, "agent_code": agent_code}
        improved_code = self.execute(input_data)
        self.agent_update_manager.update_agent(agent, improved_code, "Performance improvement")

    def load_agent_code(self, filename: str) -> str:
        with open(os.path.join(self.directory, filename), 'r') as f:
            return f.read()

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



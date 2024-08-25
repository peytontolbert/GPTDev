import openai
import os
import json
import importlib
from typing import List, Dict, Any
from chat.chat_with_ollama import ChatGPT

class GPTBuilderImprover:
    def __init__(self, agents_directory: str = "agents"):
        self.original_code = ""
        self.improved_code = ""
        self.agents_directory = agents_directory
        self.agents = self._load_agents()
        self.gpt = ChatGPT()
        self.improvement_history = []

    def _load_agents(self) -> Dict[str, Any]:
        agents = {}
        for filename in os.listdir(self.agents_directory):
            if filename.endswith("_agent.py"):
                agent_name = filename[:-3]  # Remove '.py'
                module = importlib.import_module(f'{self.agents_directory}.{agent_name}')
                agent_class = getattr(module, f'{agent_name.capitalize()}Agent', None)
                if agent_class:
                    agents[agent_name] = agent_class()
        return agents

    def load_original_code(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            self.original_code = file.read()

    def improve_builder(self, iterations: int = 3) -> str:
        current_code = self.original_code
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}")
            improvements = self._get_improvements(current_code)
            print(f"Number of improvements suggested: {len(improvements)}")
            current_code = self._apply_improvements(current_code, improvements)
            self._evaluate_improvements(current_code, improvements)
            if current_code == self.original_code:
                print("Warning: No changes were made in this iteration.")
        self.improved_code = current_code
        return self.improved_code

    def _get_improvements(self, code: str) -> List[Dict[str, Any]]:
        improvements = []
        
        # Use existing agents for specialized improvements
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'analyze_code'):
                agent_improvements = agent.analyze_code(code)
                improvements.extend(agent_improvements)
        
        # Use GPT-4 for general improvements
        gpt_improvements = self._get_gpt_improvements(code)
        improvements.extend(gpt_improvements)
        
        return improvements

    def _get_gpt_improvements(self, code: str) -> List[Dict[str, Any]]:
        prompt = f"""
        Analyze the following GPT Builder code and suggest improvements:

        {code}

        Focus on the following areas:
        1. Code structure and organization
        2. Error handling and robustness
        3. Efficiency and performance
        4. Modularity and extensibility
        5. Integration with other agents
        6. Testing and quality assurance
        7. Documentation and code readability

        Provide specific, actionable improvements in the following JSON format:
        [
            {{
                "area": "Area of improvement",
                "suggestion": "Detailed suggestion",
                "code_change": "Specific code change or addition"
            }}
        ]
        """
        system_prompt = "You are an expert Python developer specializing in AI and agent-based systems."
        response = self.gpt.chat_with_ollama(system_prompt, prompt)
        try:
            print(response)
            return json.loads(response)
        except json.JSONDecodeError:
            print("Error: GPT response is not valid JSON. Returning empty list.")
            return []

    def _evaluate_improvements(self, improved_code: str, improvements: List[Dict[str, Any]]) -> None:
        evaluation_prompt = f"""
        Evaluate the effectiveness of the following code improvements:

        Original Code:
        {self.original_code}

        Improved Code:
        {improved_code}

        Improvements Applied:
        {json.dumps(improvements, indent=2)}

        Please rate each improvement on a scale of 1-10 and provide a brief explanation.
        Return your evaluation in the following JSON format:
        [
            {{
                "improvement": "Brief description of the improvement",
                "rating": 8,
                "explanation": "Explanation of the rating"
            }}
        ]
        """
        system_prompt = "You are an expert code reviewer specializing in Python and AI systems."
        evaluation_response = self.gpt.chat_with_ollama(system_prompt, evaluation_prompt)
        evaluation = json.loads(evaluation_response)
        print(evaluation_response)
        self.improvement_history.append({
            "improvements": improvements,
            "evaluation": evaluation
        })

    def _format_improvement_history(self) -> str:
        if not self.improvement_history:
            return "No previous improvements."
        
        formatted_history = "Previous improvements and their effectiveness:\n"
        for iteration, history in enumerate(self.improvement_history, 1):
            formatted_history += f"Iteration {iteration}:\n"
            for improvement, evaluation in zip(history['improvements'], history['evaluation']):
                formatted_history += f"- {improvement['suggestion']} (Rating: {evaluation['rating']}/10)\n"
        
        return formatted_history
    def _apply_improvements(self, code: str, improvements: List[Dict[str, Any]]) -> str:
        for improvement in improvements:
            if 'code_change' in improvement and improvement['code_change']:
                try:
                    old_code, new_code = improvement['code_change'].split('Old:')[1].split('New:')
                    old_code = old_code.strip()
                    new_code = new_code.strip()
                    if old_code in code:
                        code = code.replace(old_code, new_code)
                    else:
                        print(f"Warning: Could not find the following code to replace:\n{old_code}")
                except Exception as e:
                    print(f"Error applying improvement: {str(e)}")
        return code
    def save_improved_code(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write(self.improved_code)

# Example usage
if __name__ == "__main__":
    improver = GPTBuilderImprover()
    improver.load_original_code("builder_gpt.py")
    improved_code = improver.improve_builder(iterations=3)
    improver.save_improved_code("improved_builder_gpt.py")
    print("Improvement process completed. Check 'improved_buildergpt.py' for the result.")
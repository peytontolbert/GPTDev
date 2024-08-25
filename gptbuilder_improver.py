import openai
import os
import logging
import json
import importlib
import yaml
from typing import List, Dict, Any
from chat.chat_with_ollama import ChatGPT

class GPTBuilderImprover:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.original_code = ""
        self.improved_code = ""
        self.agents_directory = self.config.get('agents_directory', 'agents')
        self.agents = self._load_agents()
        self.gpt = ChatGPT()
        self.improvement_history = []
        self.max_iterations = self.config.get('max_iterations', float('inf'))

    def load_config(self, config_path: str) -> dict:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            print(f"Warning: Config file '{config_path}' not found. Using default values.")
            return {
                'max_iterations': float('inf'),
                'agents_directory': 'agents',
                'log_file': 'gptbuilder_improver.log',
                'log_level': 'INFO'
            }

    def setup_logging(self) -> None:
        logging.basicConfig(
            filename=self.config.get('log_file', 'gptbuilder_improver.log'),
            level=getattr(logging, self.config.get('log_level', 'INFO')),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )


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

    def improve_builder(self, iterations: int = None) -> str:
        if iterations is not None:
            self.max_iterations = iterations
        current_code = self.original_code
        all_improvements = []
        self.current_iteration = 0
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            logging.info(f"Starting iteration {self.current_iteration}")
            
            try:
                improvements = self._get_improvements(current_code)
                if not improvements:
                    logging.info("No further improvements suggested. Stopping.")
                    break
                    
                selected_improvements = self._select_improvements(improvements)
                if not selected_improvements:
                    logging.info("No improvements selected. Stopping.")
                    selected_improvements = self._force_selection(improvements)
                    if not selected_improvements:
                        break
                
                all_improvements.extend(selected_improvements)
                logging.info(f"Number of improvements selected: {len(selected_improvements)}")
                    
                new_code = self._apply_improvements(current_code, selected_improvements)
                if new_code == current_code:
                    logging.info("No changes were made in this iteration. Stopping.")
                    new_code = self._make_minor_changes(current_code)
                    if new_code == current_code:
                        break
                
                current_code = new_code
                self._evaluate_improvements(current_code, selected_improvements)
            
                # Save progress after each iteration
                self._save_progress(self.current_iteration, current_code, all_improvements)
        
            except Exception as e:
                logging.error(f"Error in iteration {self.current_iteration}: {str(e)}")
                break
        self.improved_code = current_code
        self._save_improvements(all_improvements)
        return self.improved_code

    def _save_progress(self, iteration: int, current_code: str, all_improvements: List[Dict[str, Any]]) -> None:
        # Create a directory for this run if it doesn't exist
        run_dir = f"improvement_run_{self.start_time}"
        os.makedirs(run_dir, exist_ok=True)

        # Save current code
        with open(os.path.join(run_dir, f"iteration_{iteration}_code.py"), "w") as f:
            f.write(current_code)

        # Save improvements
        with open(os.path.join(run_dir, f"iteration_{iteration}_improvements.json"), "w") as f:
            json.dump(all_improvements, f, indent=2)

        # Log progress
        logging.info(f"Progress saved for iteration {iteration}")

    def _get_gpt_improvements(self, code: str) -> List[Dict[str, Any]]:
        initial_prompt = self._generate_improvement_prompt(code)
        system_prompt = "You are an expert Python developer specializing in AI and agent-based systems."
        response = self.gpt.chat_with_ollama(system_prompt, initial_prompt)
        
        try:
            improvements = json.loads(response)
            filtered_improvements = self._filter_valid_improvements(improvements)
            
            if not filtered_improvements:
                logging.warning("No valid improvements suggested by GPT. Trying meta-prompt.")
                meta_prompt = self._meta_improvement_prompt(self.current_iteration)
                meta_response = self.gpt.chat_with_ollama(system_prompt, meta_prompt)
                meta_improvements = json.loads(meta_response)
                filtered_improvements = self._filter_valid_improvements(meta_improvements)
            
            return filtered_improvements
        except json.JSONDecodeError:
            logging.error("Error: GPT response is not valid JSON. Returning empty list.")
            return []

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


    def _select_improvements(self, improvements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompt = self._generate_selection_prompt(improvements)
        system_prompt = "You are an expert code reviewer. Select the most impactful improvements."
        response = self.gpt.chat_with_ollama(system_prompt, prompt)
        
        try:
            selected_indices = json.loads(response)
            return [improvements[i] for i in selected_indices if i < len(improvements)]
        except json.JSONDecodeError:
            print("Error: GPT response is not valid JSON. Returning all improvements.")
            return improvements


    def _generate_selection_prompt(self, improvements: List[Dict[str, Any]]) -> str:
        return f"""
        Review the following code improvements and select the most impactful ones:

        {json.dumps(improvements, indent=2)}

        Return a list of indices (0-based) for the selected improvements in JSON format.
        Example: [0, 2, 4]
        """


    def _expand_improvements(self, improvements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompt = self._generate_expansion_prompt(improvements)
        system_prompt = "You are an expert Python developer. Expand on the given improvements."
        response = self.gpt.chat_with_ollama(system_prompt, prompt)
        
        try:
            expanded_improvements = json.loads(response)
            return self._filter_valid_improvements(expanded_improvements)
        except json.JSONDecodeError:
            print("Error: GPT response is not valid JSON. Returning original improvements.")
            return improvements

    def _generate_expansion_prompt(self, improvements: List[Dict[str, Any]]) -> str:
        return f"""
        Expand on the following code improvements by providing more detailed suggestions or additional related improvements:

        {json.dumps(improvements, indent=2)}

        Return the expanded list of improvements in the same JSON format.
        """

    def _generate_improvement_prompt(self, code: str) -> str:
        return f"""
        Analyze the following Python code and suggest improvements:

        {code}

        Focus on the following areas, and always suggest at least one improvement for each area:
        1. Code structure and organization
        2. Error handling and robustness
        3. Efficiency and performance
        4. Modularity and extensibility
        5. Integration with other components
        6. Testing and quality assurance
        7. Documentation and code readability

        Even if the code seems well-written, find ways to enhance it further. Consider:
        - Adding new features or capabilities
        - Improving existing functionality
        - Optimizing for better performance
        - Enhancing code clarity and maintainability
        - Introducing best practices or design patterns

        Provide specific, actionable improvements in the following JSON format:
        [
            {{
                "area": "Area of improvement",
                "suggestion": "Detailed suggestion",
                "code_change": "Old: <old_code>\nNew: <new_code>",
                "rationale": "Explanation of why this improvement is beneficial"
            }}
        ]
        """
    

    def _meta_improvement_prompt(self, iteration: int) -> str:
        return f"""
        You are an AI assistant specializing in continuous code improvement. This is iteration {iteration} of our improvement process.

        Your task is to analyze the current state of the code and suggest further improvements, no matter how small or incremental they may be. Remember that even well-written code can always be enhanced in some way.

        Consider the following strategies for finding improvements:
        1. Reflect on the code's purpose and suggest new features or capabilities that align with its goals.
        2. Identify any repeated patterns that could be abstracted into reusable functions or classes.
        3. Look for opportunities to apply advanced Python features or libraries that could simplify the code.
        4. Consider edge cases or potential issues that haven't been addressed yet.
        5. Suggest ways to make the code more scalable or adaptable to future changes.
        6. Propose improvements to the code's overall architecture or design.
        7. Identify areas where additional error handling or logging could be beneficial.
        8. Suggest performance optimizations, even for parts of the code that seem efficient.
        9. Recommend ways to enhance the code's readability or self-documentation.
        10. Propose additional tests or quality assurance measures.

        Always strive to suggest at least 3-5 meaningful improvements, even if they are small refinements.

        Provide your suggestions in the same JSON format as before.
        """


    def _filter_valid_improvements(self, improvements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [imp for imp in improvements if self._is_valid_improvement(imp)]

    def _is_valid_improvement(self, improvement: Dict[str, Any]) -> bool:
        required_keys = ['area', 'suggestion', 'code_change']
        return all(key in improvement for key in required_keys) and 'Old:' in improvement['code_change'] and 'New:' in improvement['code_change']



    def _evaluate_improvements(self, improved_code: str, improvements: List[Dict[str, Any]]) -> None:
        print(f"improved code: {improved_code}")
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

    def _force_improvements(self, code: str) -> List[Dict[str, Any]]:
        """
        Force the generation of minor improvements or even format-based changes to keep the loop going.
        """
        logging.info("Forcing minor improvements or adjustments to continue the iteration.")
        forced_improvements = [
            {
                "area": "Code readability",
                "suggestion": "Reformat code to improve readability.",
                "code_change": f"Old: {code}\nNew: {code}",  # Example: no real change, but triggers the loop
                "rationale": "Improves consistency in code format."
            }
        ]
        return forced_improvements

    def _force_selection(self, improvements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Force selection of any potential improvement to continue the cycle.
        """
        logging.info("Forcing selection of any available improvements to prevent stopping.")
        return improvements if improvements else []


    def _make_minor_changes(self, code: str) -> str:
        """
        Make minor changes, such as reformatting or renaming variables, to prompt further improvements.
        """
        logging.info("Making minor changes to the code to encourage further iterations.")
        # Example: rename a variable slightly or reformat the code
        return code  # Placeholder for an actual minor change logic


    def _save_improvements(self, improvements: List[Dict[str, Any]]) -> None:
        if not improvements:
            print("Warning: No improvements were made.")
            improvements = []
        
        with open("improvements.json", "w") as f:
            json.dump(improvements, f, indent=2)
        
        print(f"Saved {len(improvements)} improvements to improvements.json")

        
    def save_improved_code(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write(self.improved_code)
        print(f"Improved code saved to {file_path}")
        print("Improvements list saved to improvements.json")

# Example usage
if __name__ == "__main__":
    improver = GPTBuilderImprover()
    improver.load_original_code("builder_gpt.py")
    improved_code = improver.improve_builder(iterations=3)
    improver.save_improved_code("improved_builder_gpt.py")
    print("Improvement process completed. Check 'improved_builder_gpt.py' for the result and 'improvements.json' for the list of improvements.")
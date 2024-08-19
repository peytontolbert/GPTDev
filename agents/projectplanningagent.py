# Import necessary modules
import openai
import os
import json
from chat.chat_with_ollama import ChatGPT
from utils.file_utils import get_file_content, get_file_paths

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class ProjectPlanningAgent:
    def __init__(self, prompt: str, directory: str, model: str = "gpt-4-1106-preview"):
        self.prompt = prompt
        self.directory = directory
        self.gpt = ChatGPT()

    def clarify_prompt(self):
        while True:
            clarifying_prompt = (
                "Please clarify the project requirements.\n\n"
                "Is anything unclear? If yes, only answer in the form:\n"
                "{remaining unclear areas} remaining questions.\n"
                "{Next question}\n"
                "If everything is sufficiently clear, only answer 'no'."
            )
            clarifying_questions = self.gpt.chat_with_ollama_nojson(
                clarifying_prompt, self.prompt
            )
            print(clarifying_questions)
            user_input = input('(answer in text, or "q" to move on): ').strip()

            if user_input.lower() == "q":
                break

            self.prompt += f" {user_input}"
            print()

        return json.dumps(self.prompt)

    def parse_response(self, response: str | dict | list | None) -> dict | list | None:
        if isinstance(response, str):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                print("Failed to decode JSON. Handling as a string or other format.")
                return None
        elif isinstance(response, (dict, list)):
            return response
        else:
            print("Unexpected data type received.")
            return None

    def generate_plan(self):
        if not hasattr(self, "plan"):
            print("Error: 'plan' attribute is not defined.")
            return

        plan_path = os.path.join(self.directory, f"{self.prompt}_plan.json")
        try:
            with open(plan_path, "w") as file:
                json.dump(self.plan, file, indent=4)
            print(f"Project plan created: {plan_path}")
        except Exception as e:
            print(f"Failed to create project plan: {e}")

    def create_project_plan(self):
        planning_prompt = (
            """Create a detailed, purposeful plan for developing the user's project based on the following prompt:\n\n"""
            f"{self.prompt}\n\n"
            """The plan should include the following sections:\n
            1. Project Overview\n
            2. Objectives\n
            3. Key Features\n
            4. Milestones\n
            5. Timeline\n
            6. Resources Needed\n
            7. Potential Challenges and Solutions\n
            8. Next Steps\n"""
        )
        response = self.gpt.chat_with_ollama(planning_prompt)
        self.plan = self.parse_response(response)
        if self.plan:
            print("Project plan created successfully.")
        else:
            print("Failed to create project plan.")

    def write_docs_to_directory(self, path, content):
        with open(path, "w") as file:
            file.write(content)

    def is_relevant(self, file_content, natural_language_input):
        # Define the system prompt for relevance checking
        system_prompt = (
            "You are an AI assistant that helps determine the relevance of a file based on user input. "
            "The user input is as follows:\n"
            f"{natural_language_input}\n"
            "Determine if the following file content is relevant to the user's input. "
            "Respond with 'relevant' or 'not relevant'."
        )

        # Use chat_with_ollama to determine relevance
        response = self.gpt.chat_with_ollama(system_prompt, file_content)
        return "relevant" in response.lower()

    def gather_relevant_parts(
        self,
        directory,
        natural_language_input,
        extensions=[".py", ".md", ".txt"],
        max_depth=3,
        current_depth=0,
    ):
        if current_depth > max_depth:
            return ""

        file_paths = get_file_paths(directory, extensions)
        context = ""
        for path in file_paths:
            file_content = get_file_content(path)
            if self.is_relevant(file_content, natural_language_input):
                context += f"File: {path}\n"
                context += file_content + "\n\n"

        subdirectories = [
            os.path.join(directory, d)
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]
        for subdirectory in subdirectories:
            context += self.gather_relevant_parts(
                subdirectory,
                natural_language_input,
                extensions,
                max_depth,
                current_depth + 1,
            )

        return context

    def modify_project(self, project, natural_language_input):
        # Define the system prompt
        system_prompt = (
            "You are an AI assistant that helps modify project plans based on user input. "
            "The project structure is as follows:\n"
            "{'name': 'Project Name', 'description': 'Project Description', 'tasks': [{'name': 'Task 1', 'description': 'Task 1 Description'}, {'name': 'Task 2', 'description': 'Task 2 Description'}]}\n"
            "Modify the project based on the user's natural language input."
        )

        # Gather relevant context from the codebase
        context = self.gather_relevant_parts(self.directory)

        # Use chat_with_ollama to process the natural language input with context
        response = self.gpt.chat_with_ollama(
            system_prompt + context, natural_language_input
        )
        parsed_response = self.parse_response(response)

        if not parsed_response:
            return "Failed to process the input with chat_with_ollama."

        # Modify the project based on the parsed response
        for key, value in parsed_response.items():
            if key in project:
                project[key] = value
            else:
                # Check if the key is a task name
                for task in project["tasks"]:
                    if task["name"] == key:
                        task["name"] = value
                        break
                else:
                    return f"Component '{key}' not found in the project."

        return project

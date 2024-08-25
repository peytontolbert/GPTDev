from agents.base_agent import Agent
from agents.communication.prompt_clarification_agent import PromptClarificationAgent
from agents.documentation.documentation_generation_agent import DocumentationGenerationAgent
from agents.improvement.code_modification_agent import CodeModificationAgent
from agents.integration.code_integration_agent import CodeIntegrationAgent
from agents.testing.testing_agent import TestingAgent

class CodebaseModificationAgent(Agent):
    def __init__(self, name, prompt, directory):
        super().__init__(name)
        self.prompt = prompt
        self.directory = directory
        self.prompt_clarification_agent = PromptClarificationAgent()
        self.documentation_generation_agent = DocumentationGenerationAgent()
        self.code_modification_agent = CodeModificationAgent()
        self.code_integration_agent = CodeIntegrationAgent()
        self.testing_agent = TestingAgent()

    def execute(self, input_data):
        self.perform_task(input_data)

    def generate_prompt(self, input_data):
        return f"Modify the codebase in the directory {self.directory} based on the following prompt: {self.prompt}"

    def perform_task(self, input_data):
        self.prompt = self.prompt_clarification_agent.clarify_prompt(self.prompt)
        self.documentation_generation_agent.generate_readme_and_docs(self.prompt, self.directory)
        self.edit_codebase()
        self.testing_agent.run_tests(self.directory)

    def edit_codebase(self):
        file_paths = get_file_paths(self.directory)
        for file_path in file_paths:
            content = get_file_content(file_path)
            edited_content = self.code_modification_agent.perform_task(content, self.prompt)
            write_file(file_path, edited_content)

    def create_temp_directory(self):
        temp_dir = tempfile.mkdtemp()
        for file_path in get_file_paths(self.directory):
            shutil.copy(file_path, temp_dir)
        return temp_dir

    def clarify_prompt(self):
        while True:
            clarifying_prompt = (
                "Is anything unclear? If yes, only answer in the form:\n"
                "{remaining unclear areas} remaining questions. \n"
                "{Next question}\n"
                "If everything is sufficiently clear, only answer 'no'."
            )
            response = openai.Completion.create(
                model=self.model,
                prompt=f"{clarifying_prompt}\n\n{self.prompt}",
                max_tokens=150,
            )
            clarifying_questions = response.choices[0].text.strip()
            print(clarifying_questions)
            user_input = input('(answer in text, or "q" to move on)\n')
            self.prompt += user_input
            print()

            if not user_input or user_input.strip().lower() == "q":
                break
        return json.dumps(self.prompt)

    def parse_response(self, response):
        if response and isinstance(response, str):
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

    def find_relevant_portions(self, content):
        response = self.gpt.chat_with_ollama(system_prompt, prompt)
        return response.choices[0].text.strip().split("\n")

    def test_integrations(self):
        os.system("pytest")


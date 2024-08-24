### Documentation for `agents` Directory
A suite of agents that can facilitate fully end to end software development
---

#### `base_agent.py`

---

##### `Agent`
**Description**: 
The `Agent` class serves as a base class for all agents. It provides common functionalities such as prompt generation, response parsing, and logging.

**Attributes**:
- `name`: The name of the agent.
- `gpt`: An instance of the `ChatGPT` class for interacting with the GPT model.

**Methods**:

---

##### `__init__(self, name)`
**Description**: 
Initializes the `Agent` with the given name.

**Parameters**:
- `name`: The name of the agent.

---

##### `execute(self, input_data)`
**Description**: 
Abstract method that must be implemented by each agent to execute a task based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

---

##### `generate_prompt(self, input_data)`
**Description**: 
Abstract method that must be implemented by each agent to generate a prompt based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

---

##### `clarify_prompt(self, prompt)`
**Description**: 
Clarifies the prompt by asking the user for additional information if needed.

**Parameters**:
- `prompt`: The initial prompt that needs clarification.

**Returns**: 
A clarified prompt.

---

##### `parse_response(self, response)`
**Description**: 
Parses the response from the GPT model.

**Parameters**:
- `response`: The response from the GPT model.

**Returns**: 
A dictionary representing the parsed response.

---

##### `log(self, message)`
**Description**: 
Logs a message with the agent's name.

**Parameters**:
- `message`: The message to log.

---

##### `save_to_file(self, filename, content)`
**Description**: 
Saves the provided content to the specified file path.

**Parameters**:
- `filename`: The file path where the content is to be written.
- `content`: The content to be written.

---

#### `bugtracking_agent.py`

---

##### `BugTrackingAgent`
**Description**: 
The `BugTrackingAgent` class integrates with bug tracking systems to manage and prioritize bug fixes.

**Attributes**:
- `name`: The name of the agent.
- `gpt`: An instance of the `ChatGPT` class for interacting with the GPT model.

**Methods**:

---

##### `__init__(self, name)`
**Description**: 
Initializes the `BugTrackingAgent` with the given name.

**Parameters**:
- `name`: The name of the agent.

---

##### `execute(self, input_data)`
**Description**: 
Executes the task of managing and prioritizing bug fixes based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
A detailed plan of action for managing and prioritizing bug fixes.

---

##### `generate_prompt(self, input_data)`
**Description**: 
Generates a prompt for managing and prioritizing bug fixes based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
A prompt for the GPT model.

---

##### `perform_task(self, input_data)`
**Description**: 
Performs the task of managing and prioritizing bug fixes by generating a prompt and processing the response from the GPT model.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
A dictionary representing the parsed response.

---

##### `parse_response(self, response)`
**Description**: 
Parses the response from the GPT model.

**Parameters**:
- `response`: The response from the GPT model.

**Returns**: 
A dictionary representing the parsed response.

---

#### `full_codebasegen_agent.py`

---

##### `GenerateCodebaseAgent`
**Description**: 
The `GenerateCodebaseAgent` class is responsible for generating a codebase based on a given prompt. It interacts with various agents to clarify the prompt, parse responses, and generate documentation.

**Attributes**:
- `prompt`: The initial prompt provided to the agent.
- `directory`: The directory where the generated codebase will be stored.
- `gpt`: An instance of the `ChatGPT` class for interacting with the GPT model.

**Methods**:

---

##### `__init__(self, prompt, directory, model=DEFAULT_MODEL)`
**Description**: 
Initializes the `GenerateCodebaseAgent` with the given prompt, directory, and model.

**Parameters**:
- `prompt`: The initial prompt provided to the agent.
- `directory`: The directory where the generated codebase will be stored.
- `model`: The model to be used for generating the codebase (default is `DEFAULT_MODEL`).

---

##### `clarify_prompt(self)`
**Description**: 
Interacts with the `clarifying_agent` to clarify the initial prompt. The user can provide additional input to refine the prompt.

**Returns**: 
A JSON string of the clarified prompt.

---

##### `parse_response(self, response)`
**Description**: 
Parses the response from the GPT model. If the response is a valid JSON string, it is parsed into a dictionary. If the response is already a dictionary or list, it is returned directly. Otherwise, an error message is printed.

**Parameters**:
- `response`: The response from the GPT model.

**Returns**: 
A dictionary or list representing the parsed response, or `None` if the response could not be parsed.

---

##### `update_documentation(self, shared_dependencies, filepaths)`
**Description**: 
Generates detailed documentation for the project, including shared dependencies and file paths. The documentation is appended to the `DOCUMENTATION.md` file.

**Parameters**:
- `shared_dependencies`: A dictionary representing shared dependencies.
- `filepaths`: A list of file paths in the project.

---

##### `generate_codebase(self, prompt)`
**Description**: 
Main orchestration method to generate the entire codebase based on the provided prompt.

**Parameters**:
- `prompt`: The initial prompt provided to the agent.

**Returns**: 
None

---

#### `codebasemodification_agent.py`

---

##### `CodebaseModificationAgent`
**Description**: 
The `CodebaseModificationAgent` class is responsible for modifying a codebase based on a given prompt. It interacts with the user to clarify the prompt, generates edits for the codebase, and runs tests to ensure the changes are correct.

**Attributes**:
- `prompt`: The initial prompt provided to the agent.
- `directory`: The directory of the codebase to be edited.
- `gpt`: An instance of the `ChatGPT` class for interacting with the GPT model.

**Methods**:

---

##### `__init__(self, prompt: str, directory: str, model: str = "gpt-4-1106-preview")`
**Description**: 
Initializes the `CodebaseModificationAgent` with the given prompt, directory, and model.

**Parameters**:
- `prompt`: The user prompt for editing the codebase.
- `directory`: The directory of the codebase to be edited.
- `model`: The model to be used for generating edits (default is "gpt-4-1106-preview").

---

##### `perform_task(self, input_data)`
**Description**: 
Performs the task of modifying the codebase based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
None

---

##### `generate_prompt(self, input_data)`
**Description**: 
Generates a prompt for modifying the codebase based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
A prompt for the GPT model.

---

##### `edit_and_test_codebase(self)`
**Description**: 
Edits the codebase in a temporary directory and runs tests. If the tests pass, the original files are replaced with the modified files. If the tests fail, the original codebase remains unchanged.

---

##### `create_temp_directory(self)`
**Description**: 
Creates a temporary directory and copies the original files into it.

**Returns**: 
A string representing the path to the temporary directory.

---

##### `clarify_prompt(self)`
**Description**: 
Clarifies the prompt by asking the user for additional information if needed. The method interacts with the user to ensure that the prompt is clear and complete, appending user responses to the prompt until no further clarification is needed.

**Returns**: 
A JSON string of the clarified prompt.

---

##### `parse_response(self, response)`
**Description**: 
Parses the response from the GPT model. If the response is a valid JSON string, it is parsed into a dictionary. If the response is already a dictionary or list, it is returned directly. Otherwise, an error message is printed.

**Parameters**:
- `response`: The response from the GPT model.

**Returns**: 
A dictionary or list representing the parsed response, or `None` if the response could not be parsed.

---

##### `generate_readme_and_docs(self)`
**Description**: 
Generates a `README.md` and `DOCUMENTATION.md` file in the specified directory. The `README.md` contains an overview of the project, and the `DOCUMENTATION.md` contains a placeholder for detailed documentation.

---

##### `write_docs_to_directory(self, path, content)`
**Description**: 
Writes the provided content to the specified file path.

**Parameters**:
- `path`: The file path where the content is to be written.
- `content`: The content to be written.

---

##### `edit_codebase(self)`
**Description**: 
Edits the codebase based on the prompt. This method retrieves all file paths in the specified directory, generates edits for each file, and writes the edited content back to the files.

---

##### `generate_edit(self, content: str) -> str`
**Description**: 
Generates the edited content based on the prompt using the GPT model.

**Parameters**:
- `content`: The original content of the file.

**Returns**: 
A string representing the edited content generated by the GPT model.

---

##### `find_relevant_portions(self, content: str) -> List[str]`
**Description**: 
Finds relevant portions of the code to be modified based on the prompt.

**Parameters**:
- `content`: The original content of the file.

**Returns**: 
A list of relevant portions of the code to be modified.

---

##### `test_integrations(self)`
**Description**: 
Runs tests to ensure the changes do not break the codebase. This method runs the test suite using pytest to verify that the changes made to the codebase do not introduce any new issues or break existing functionality.

---

#### `orchestration_agent.py`

---

##### `OrchestrationAgent`
**Description**: 
The `OrchestrationAgent` class is responsible for coordinating the activities of multiple agents to achieve complex tasks.

**Attributes**:
- `name`: The name of the agent.
- `agents`: A dictionary of agent instances that the orchestration agent can coordinate.
- `gpt`: An instance of the `ChatGPT` class for interacting with the GPT model.

**Methods**:

---

##### `__init__(self, name, agents)`
**Description**: 
Initializes the `OrchestrationAgent` with the given name and a dictionary of agents.

**Parameters**:
- `name`: The name of the agent.
- `agents`: A dictionary of agent instances that the orchestration agent can coordinate.

---

##### `execute(self, input_data)`
**Description**: 
Executes the task of coordinating multiple agents based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
A dictionary of results from the coordinated agents.

---

##### `generate_task_plan(self, input_data)`
**Description**: 
Generates a task plan with specific agents to accomplish the tasks based on the input data.

**Parameters**:
- `input_data`: The input data for the agent to process.

**Returns**: 
A dictionary representing the task plan.

---

##### `parse_response(self, response)`
**Description**: 
Parses the response from the GPT model.

**Parameters**:
- `response`: The response from the GPT model.

**Returns**: 
A dictionary representing the parsed response.

---



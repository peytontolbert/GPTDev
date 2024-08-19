
### Documentation for `agents` Directory

---

#### `codeagents.py`

---

##### `code_understanding_agent()`
**Description**: 
This function returns a prompt for an AI specializing in code comprehension. The AI is tasked with examining the given code and elucidating its purpose and core functionality. The understanding is returned as a Python dictionary.

---

##### `code_error_detection_agent()`
**Description**: 
This function returns a prompt for an AI expert in identifying code errors. The AI analyzes the provided code and pinpoints any anomalies or mistakes, expressing the findings as a Python dictionary.

---

##### `code_testing_agent()`
**Description**: 
This function returns a prompt for an AI adept in testing code. The AI creates appropriate test cases for the provided code and compiles the results into a Python dictionary.

---

##### `code_optimization_agent()`
**Description**: 
This function returns a prompt for an AI proficient in code optimization. The AI optimizes the provided code and returns the enhanced code as a Python dictionary.

---

##### `code_documentation_agent()`
**Description**: 
This function returns a prompt for an AI expert in code documentation. The AI generates comprehensive documentation for the provided code, including necessary modules and packages like `os`, `glob`, `dotenv`, and others. The resulting documentation is formatted as a Python dictionary.

---

##### `code_algorithm_agent()`
**Description**: 
This function returns a prompt for an AI specialized in algorithm understanding and explanation. The AI scrutinizes the provided code and unravels the algorithmic methodology employed, considering aspects like complexity, employed data structures, and the logic of the code. The explanation is formatted in a manner that can be included in a human-readable prompt and presented as a Python dictionary.

---

##### `code_design_agent()`
**Description**: 
This function returns a prompt for an AI expert in system design and architecture. The AI dissects the provided code and sketches its system design, considering components such as classes and their interrelationships, data flow, and the overarching structure of the code. The findings are packaged into a Python dictionary.

---

##### `code_prompt_agent()`
**Description**: 
This function returns a prompt for an AI that excels in crafting prompt text for code. The AI generates a detailed prompt for the provided system algorithms and design, developing requirements that would allow a developer to reconstruct the same operational program given the details provided. The response is formatted as a Python dictionary.

---

### Documentation for `codebasegenagent.py`

---

#### `GenerateCodebaseAgent`
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

##### `generate_readme_and_docs(self)`
**Description**: 
Generates a `README.md` and `DOCUMENTATION.md` file in the specified directory. The `README.md` contains an overview of the project, and the `DOCUMENTATION.md` contains a placeholder for detailed documentation.

---

##### `update_readme(self, program_structure)`
**Description**: 
Generates a summary of the program's architecture, including the purpose of each module, class, and their relationships. The summary is appended to the `README.md` file.

**Parameters**:
- `program_structure`: A dictionary representing the program's structure.

---

##### `update_documentation(self, shared_dependencies, filepaths)`
**Description**: 
Generates detailed explanations of shared dependencies and file paths. The details are appended to the `DOCUMENTATION.md` file.

**Parameters**:
- `shared_dependencies`: A dictionary representing the shared dependencies.
- `filepaths`: A list of file paths in the program.

---

##### `update_readme_for_code(self, filecode)`
**Description**: 
Generates a summary of the provided code, including its main components and purpose. The summary is appended to the `README.md` file.

**Parameters**:
- `filecode`: The code for which the summary is to be generated.

---

##### `update_documentation_for_code(self, filecode)`
**Description**: 
Generates detailed explanations of the provided code's implementation, including key functions, logic flow, and significant design decisions. The details are appended to the `DOCUMENTATION.md` file.

**Parameters**:
- `filecode`: The code for which the implementation details are to be generated.

---

##### `design_program_structure(self)`
**Description**: 
Designs the program structure based on the clarified requirements. The design includes modules, classes, functions, relationships, and data flow, presented in a structured JSON format.

**Returns**: 
A dictionary representing the program's design.

---

##### `generate_file_paths(self, program_structure, initial_dependencies, readme)`
**Description**: 
Generates a list of file paths based on the program structure and initial dependencies. The file paths are created to match the user's intent and project overview.

**Parameters**:
- `program_structure`: The structure of the program in JSON format.
- `initial_dependencies`: The initial dependencies for the program.
- `readme`: The README content for the project.

---

##### `parse_filepath_list(self, result)`
**Description**: 
Parses a string result to extract a list of file paths. The method handles different formats and attempts to evaluate the string as a Python list.

**Parameters**:
- `result`: The string result to be parsed.

**Returns**: 
A list of file paths.

---

##### `generate_shared_dependencies(self, program_structure, readme)`
**Description**: 
Generates shared dependencies required across the codebase based on the program structure and README content. The dependencies include shared variables, common utility functions, data schemas, interfaces, and classes.

**Parameters**:
- `program_structure`: The structure of the program in JSON format.
- `readme`: The README content for the project.

**Returns**: 
A JSON string representing the shared dependencies.

---

##### `refine_shared_dependencies(self, filepaths, program_structure)`
**Description**: 
Refines the shared dependencies based on actual file paths and program structure. The method identifies common utilities or classes from the file paths or structure analysis.

**Parameters**:
- `filepaths`: A list of file paths in the program.
- `program_structure`: The structure of the program in JSON format.

**Returns**: 
A dictionary representing the refined shared dependencies.

---

##### `generate_code_for_each_file(self, filepaths_string, program_structure, shared_dependencies=None)`
**Description**: 
Generates the main code and unit tests for each file based on the program structure and shared dependencies. The code and unit tests are written to the specified directory.

**Parameters**:
- `filepaths_string`: A string listing the file paths to be generated.
- `program_structure`: The structure of the program in JSON format.
- `shared_dependencies`: The shared dependencies for the program (default is `None`).

**Returns**: 
A tuple containing the main code and unit tests.

---

##### `AI_generate_code_and_tests(self, filepath, program_structure, shared_dependencies=None)`
**Description**: 
Generates the main code and unit tests for a specific file based on the program structure and shared dependencies. The code and unit tests are generated using the GPT model.

**Parameters**:
- `filepath`: The file path for which the code and unit tests are to be generated.
- `program_structure`: The structure of the program in JSON format.
- `shared_dependencies`: The shared dependencies for the program (default is `None`).

**Returns**: 
A tuple containing the main code and unit tests.

---

##### `write_code_and_tests(self, filepaths_string, main_code, unit_tests_code)`
**Description**: 
Writes the main code and unit tests to the specified directory.

**Parameters**:
- `filepaths_string`: A string listing the file paths to be generated.
- `main_code`: The main code to be written.
- `unit_tests_code`: The unit tests to be written.

---

##### `write_docs_to_directory(self, filepath, filecode)`
**Description**: 
Writes the provided code to the specified file path in the directory.

**Parameters**:
- `filepath`: The file path where the code is to be written.
- `filecode`: The code to be written.

---

##### `write_files_to_directory(self, filepath, filecode)`
**Description**: 
Writes the provided code to the specified file path in the directory, ensuring the directory exists.

**Parameters**:
- `filepath`: The file path where the code is to be written.
- `filecode`: The code to be written.

---

##### `debug_generated_code(self)`
**Description**: 
Debugs the generated code by identifying and fixing issues in the code files. The method iterates through code files, logs debug information, and tracks the number of failures for each function.

---

##### `filter_filepaths(filepaths)`
**Description**: 
Filters a list of file paths, removing leading slashes.

**Parameters**:
- `filepaths`: A string representation of a list of file paths.

**Returns**: 
A list of file paths with leading slashes removed.

---

##### `generate_codebase(self, prompt)`
**Description**: 
Main orchestration method to generate the entire codebase. It clarifies the prompt, generates the README and documentation, designs the program structure, generates shared dependencies, generates file paths, refines shared dependencies, generates code for each file, and debugs the generated code.

**Parameters**:
- `prompt`: The initial prompt provided to the agent.

---

### Documentation for `codingagents.py`

---

#### `requirements_agent`
**Description**: 
An instance of `ChatGPTAgent` that specializes in software requirements analysis. It transforms user needs and constraints into a formal list of software requirements, detailing functional, non-functional, and system requirements.

---

#### `design_agent()`
**Description**: 
Returns a prompt for an AI specializing in software system design. The AI creates a comprehensive system design based on provided requirements, including system architecture, software modules, their interactions, and database schema if necessary. The design is returned as a Python dictionary.

---

#### `algorithm_agent()`
**Description**: 
Returns a prompt for an AI specializing in algorithm development. The AI creates detailed algorithms based on the system design and software requirements, representing the logic and operations of each module. The algorithms are returned as a Python dictionary.

---

#### `coding_agent()`
**Description**: 
Returns a prompt for an AI specializing in software coding. The AI generates the actual code for the software based on provided algorithms and system design. The code is produced in chunks, each of which can be independently compiled and tested. The code chunks are returned as a list of strings.

---

#### `debug_agent()`
**Description**: 
Returns a prompt for an AI specializing in software debugging. The AI debugs the provided code chunks into a complete software system. Only the code that needs to be changed is returned, formatted as a Python object with the filename as the key and the code as the content.

---

#### `file_code_agent(filepaths_string, shared_dependencies)`
**Description**: 
Returns a prompt for an AI developer who generates code based on user intent. The AI writes valid code for the given file paths and shared dependencies, returning only the code without any additional explanation.

**Parameters**:
- `filepaths_string`: A string listing the file paths to be generated.
- `shared_dependencies`: A string listing the shared dependencies like filenames and variable names.

---

#### `unit_test_agent()`
**Description**: 
Returns a prompt for an AI specializing in software debugging. The AI debugs the provided code chunks into a complete software system, producing self-contained pieces of code that can be put together to form the complete software. Only the code that needs to be changed is returned, formatted as a Python object with the filename as the key and the code as the content.

---

#### `clarifying_agent()`
**Description**: 
Returns a prompt for an AI designed to clarify the user's intent. The AI summarizes areas that need clarification and asks clarifying questions for each area, waiting for an answer from the user.

---

### Documentation for `editcodebase.py`

---

#### `EditCodebaseAgent`
**Description**: 
The `EditCodebaseAgent` class is responsible for editing a codebase based on a given prompt. It interacts with the user to clarify the prompt, generates edits for the codebase, and runs tests to ensure the changes are correct.

**Attributes**:
- `prompt`: The initial prompt provided to the agent.
- `directory`: The directory of the codebase to be edited.
- `gpt`: An instance of the `ChatGPT` class for interacting with the GPT model.

**Methods**:

---

##### `__init__(self, prompt: str, directory: str, model: str = "gpt-4-1106-preview")`
**Description**: 
Initializes the `EditCodebaseAgent` with the given prompt, directory, and model.

**Parameters**:
- `prompt`: The user prompt for editing the codebase.
- `directory`: The directory of the codebase to be edited.
- `model`: The model to be used for generating edits (default is "gpt-4-1106-preview").

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
Parses the response from the OpenAI API. If the response is a valid JSON string, it is parsed into a dictionary. If the response is already a dictionary or list, it is returned directly. Otherwise, an error message is printed.

**Parameters**:
- `response`: The response from the OpenAI API.

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
Generates the edited content based on the prompt using the OpenAI API.

**Parameters**:
- `content`: The original content of the file.

**Returns**: 
A string representing the edited content generated by the OpenAI API.

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

# Agents Documentation

## Analysis

### CodebasetoPromptAgent
- **File**: `agents/analysis/codebasetoprompt_agent.py`
- **Description**: An agent that converts code into prompts suitable for AI models.
- **Class**: `CodebasetoPromptAgent`
- **Methods**:
  - `__init__(self, token_limit: int = 50000)`: Initializes the agent with a token limit.
  - `perform_task(self, directory)`: Performs the task of generating prompts for files in a directory.
  - `generate_prompt(self, input_data)`: Generates a prompt from input data.
  - `generate_prompts_for_files(self, code_files: List[str], clone_dir: str)`: Generates prompts from code files and saves them to a file.
  - `_process_and_save_prompts(self, all_funcs: List[Dict[str, str]], all_docs: List[Dict[str, str]], clone_dir: str)`: Processes documentation data and generates prompts based on token limits.
  - `_chunk_and_summarize(self, code_file: str)`: Chunks code into smaller parts and summarizes each part.
  - `_save_prompts_to_file(self, prompts: List[str], filename: str)`: Saves the generated prompts to a text file.

### DebuggingAgent
- **File**: `agents/analysis/codebase_debugging_agent.py`
- **Description**: An agent that debugs generated code.
- **Class**: `DebuggingAgent`
- **Methods**:
  - `__init__(self, name, directory)`: Initializes the agent with a name and directory.
  - `execute(self, input_data)`: Executes the debugging process.
  - `generate_prompt(self, input_data)`: Generates a prompt from input data.
  - `debug_generated_code(self, input_data)`: Debugs the generated code.

### CodeReviewAgent
- **File**: `agents/analysis/codereview_agent.py`
- **Description**: An agent that reviews inputted code to give a solid response for a Software Engineering GPT Agent.
- **Class**: `CodeReviewAgent`
- **Methods**:
  - `__init__(self)`: Initializes the agent.
  - `perform_task(self, input_data)`: Performs the task of reviewing code.
  - `generate_prompt(self, input_data)`: Generates a prompt to review the code.

### CodeUnderstandingAgent
- **File**: `agents/analysis/codeunderstanding_agent.py`
- **Description**: An agent that has the knowledge of a Software Development GPT Agent to understand and explain a given piece of code.
- **Class**: `CodeUnderstandingAgent`
- **Methods**:
  - `__init__(self)`: Initializes the agent.
  - `generate_prompt(self, code)`: Generates a prompt to understand the code.
  - `perform_task(self, code)`: Performs the task of understanding the code.
  - `parse_response(self, response)`: Parses the response from the GPT model.

### CodeAnalysisAgent
- **File**: `agents/analysis/code_analysis_agent.py`
- **Description**: An agent that analyzes code and identifies any issues.
- **Class**: `CodeAnalysisAgent`
- **Methods**:
  - `__init__(self, name)`: Initializes the agent with a name.
  - `analyze_code(self, code)`: Analyzes the given code and identifies any issues.
  - `execute(self, input_data)`: Executes the code analysis process.
  - `generate_prompt(self, input_data)`: Generates a prompt for code analysis.


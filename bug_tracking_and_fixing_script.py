from agents.bugtracking_agent import BugTrackingAgent
from agents.codebase_debugging_agent import CodebaseDebuggingAgent
from agents.code_generation_agent import CodeGenerationAgent

# Initialize agents
bug_tracking_agent = BugTrackingAgent('BugTrackingAgent')
codebase_debugging_agent = CodebaseDebuggingAgent('CodebaseDebuggingAgent')
code_generation_agent = CodeGenerationAgent('CodeGenerationAgent')

# Define the main function
def main(directory, prompt=None):
    # Step 1: Track bugs
    bugs = bug_tracking_agent.execute(directory)
    
    # Step 2: Debug the code
    debugged_code = codebase_debugging_agent.execute(bugs)
    
    # Step 3: Generate fixes
    fixed_code = code_generation_agent.execute(debugged_code, prompt)
    
    # Save the fixed code
    with open(f'{directory}/fixed_code.py', 'w') as code_file:
        code_file.write(fixed_code)

# Example usage
if __name__ == '__main__':
    example_directory = 'path/to/codebase'
    example_prompt = 'Fix the identified bugs and improve code quality.'
    main(example_directory, example_prompt)


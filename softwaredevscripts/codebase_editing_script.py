from agents.codebasemodification_agent import CodebaseModificationAgent
from agents.code_generation_agent import CodeGenerationAgent

# Initialize agents
codebase_modification_agent = CodebaseModificationAgent('CodebaseModificationAgent')
code_generation_agent = CodeGenerationAgent('CodeGenerationAgent')

# Define the main function
def main(directory, prompt):
    # Step 1: Modify the codebase based on the prompt
    modified_codebase = codebase_modification_agent.execute(directory, prompt)
    
    # Step 2: Generate new code based on the modified codebase
    generated_code = code_generation_agent.execute(modified_codebase, prompt)
    
    # Save the generated code
    with open(f'{directory}/generated_code.py', 'w') as code_file:
        code_file.write(generated_code)

# Example usage
if __name__ == '__main__':
    example_directory = 'path/to/codebase'
    example_prompt = 'Refactor the codebase to improve readability and maintainability.'
    main(example_directory, example_prompt)


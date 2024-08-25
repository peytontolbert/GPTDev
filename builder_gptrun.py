import os
from builder_gpt import BuilderGPT

def main():
    print("Welcome to BuilderGPT! I will automatically handle any software engineering task you provide.")

    # Define the directory where agents will be stored
    agents_directory = "./agents"
    
    # Ensure the agents directory exists
    os.makedirs(agents_directory, exist_ok=True)

    # Initialize BuilderGPT
    builder_gpt = BuilderGPT(
        name="AutomatedSoftwareEngineer",
        prompt="Automatically handle software engineering tasks such as model modification, codebase generation, documentation, etc.",
        directory=agents_directory
    )

    while True:
        # Get natural language input from the user
        input_requirements = input("\nDescribe the software engineering task you want me to perform (or type 'exit' to quit):\n")
        
        if input_requirements.lower() == 'exit':
            print("Exiting BuilderGPT. Goodbye!")
            break

        # Automatically determine and execute the task
        builder_gpt.execute_task(input_requirements)

def automated_task_execution(task_description: str, agents_directory: str = "./agents"):
    """Automates task execution based on natural language description."""
    
    # Ensure the agents directory exists
    os.makedirs(agents_directory, exist_ok=True)

    # Initialize BuilderGPT
    builder_gpt = BuilderGPT(
        name="AutomatedSoftwareEngineer",
        prompt="Automatically handle software engineering tasks such as model modification, codebase generation, documentation, etc.",
        directory=agents_directory
    )

    # Run BuilderGPT with the provided task description
    results = builder_gpt.execute(task_description)

    # Print out the results
    print("Task executed successfully. Here are the results:")
    for result in results:
        print(f"Agent Result: {result}")

# Example of full automation without user interaction
if __name__ == "__main__":
    task_description = """
    1. Modify a PyTorch transformer model architecture to include an additional attention head.
    2. Generate a codebase for a basic web application in Flask.
    3. Document the newly generated codebase, including installation instructions and API documentation.
    4. Update the codebase to include a new feature for user authentication.
    5. Write unit tests for the user authentication feature.
    """
    automated_task_execution(task_description)

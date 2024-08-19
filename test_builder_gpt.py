from start_largecode import CodebaseGenerator

# Define a sample prompt and directory for testing
sample_prompt = "Create a simple Python script that prints 'Hello, World!'"
test_directory = "./test_codebase"

# Instantiate the CodebaseGenerator class
generator = CodebaseGenerator(sample_prompt, test_directory)

# Design the program structure
program_structure = generator.design_program_structure()

# Generate file paths based on the program structure
file_paths = generator.generate_file_paths(program_structure)

# Create the files and write initial code
for file_path in file_paths:
    write_file(file_path, "# Initial code")

# Evaluate the generated code
evaluation_results = generator.evaluate_generated_code(test_directory)
print("Evaluation Results:", evaluation_results)

# Improve the generated code based on evaluation results
generator.improve_code(test_directory)

# Re-evaluate the improved code
improved_evaluation_results = generator.evaluate_generated_code(test_directory)
print("Improved Evaluation Results:", improved_evaluation_results)

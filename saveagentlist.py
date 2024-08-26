import os

def list_python_files(directory):
    """
    Lists all Python files in the given directory and its subdirectories.
    :param directory: The root directory to search for Python files.
    :return: A list of paths to Python files.
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)
    
    return python_files

def save_to_file(file_path, lines):
    """
    Saves a list of strings to a specified file.
    :param file_path: The path to the file where the lines will be saved.
    :param lines: The list of strings to write to the file.
    """
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(f"{line}\n")

def main():
    # Set the path to your 'agents' directory
    agents_directory = 'agents'
    
    # Get a list of all Python files in the directory
    python_files = list_python_files(agents_directory)
    
    # Save the list of Python files to 'agents_list.txt'
    output_file = 'agents_list.txt'
    save_to_file(output_file, python_files)
    
    print(f"List of Python files has been saved to {output_file}")

if __name__ == "__main__":
    main()

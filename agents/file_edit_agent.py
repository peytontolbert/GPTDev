class FileEditAgent:
    def __init__(self):
        pass

    def edit_file(self, file_path, new_content):
        try:
            with open(file_path, 'w') as file:
                file.write(new_content)
            return f"File at {file_path} has been edited."
        except Exception as e:
            return f"Failed to edit file: {str(e)}"

# Example usage
if __name__ == "__main__":
    agent = FileEditAgent()
    response = agent.edit_file('example.txt', 'This is the new content of the example file.')
    print(response)


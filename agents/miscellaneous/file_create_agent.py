class FileCreateAgent:
    def __init__(self):
        pass

    def create_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return f"File created at {file_path}"
        except Exception as e:
            return f"Failed to create file: {str(e)}"

# Example usage
if __name__ == "__main__":
    agent = FileCreateAgent()
    response = agent.create_file('example.txt', 'This is an example file.')
    print(response)


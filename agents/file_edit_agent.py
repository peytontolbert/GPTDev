import os

class FileEditAgent:
    def __init__(self):
        pass

    def edit_file(self, file_path, new_content):
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as file:
                file.write(new_content)
            return f"File at {file_path} has been edited."
        except Exception as e:
            return f"Failed to edit file: {str(e)}"

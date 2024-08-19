# Import necessary modules
import os
import json
from utils.file_utils import write_file, get_file_content, get_file_paths


class DocumentationAgent:
    def __init__(self, directory):
        self.directory = directory

    def generate_readme(self):
        readme_content = (
            f"# Project Overview\n\n"
            f"## Directory Structure\n"
            f"{self.get_directory_structure()}\n"
        )
        readme_path = os.path.join(self.directory, "README.md")
        self.write_docs_to_directory(readme_path, readme_content)
        print(f"README.md created in {self.directory}")

    def generate_documentation(self):
        documentation_content = (
            "# Documentation\n\n"
            "## Overview\n"
            "Detailed documentation will be provided here as the project structure evolves.\n"
        )
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        self.write_docs_to_directory(documentation_path, documentation_content)
        print(f"DOCUMENTATION.md created in {self.directory}")

    def get_directory_structure(self):
        file_paths = get_file_paths(self.directory, extensions=[".py", ".md", ".txt"])
        structure = ""
        for path in file_paths:
            structure += f"{path}\n"
        return structure

    def write_docs_to_directory(self, path, content):
        write_file(path, content)

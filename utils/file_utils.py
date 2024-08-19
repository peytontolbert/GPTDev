import os
import json


def get_file_paths(directory, extensions):
    """
    Get all file paths in a directory with the given extensions.

    Parameters:
    directory (str): The directory to search in.
    extensions (list): List of file extensions to include.

    Returns:
    list: List of file paths.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(root, file))
    return file_paths


def get_file_content(file_path):
    """
    Get the content of a file.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: The content of the file.
    """
    with open(file_path, "r") as file:
        return file.read()


def save_embedded_code(data, directory, subdir, file_type):
    """
    Save embedded code data to a file.

    Parameters:
    data (list): The data to save.
    directory (str): The directory to save the file in.
    subdir (str): The subdirectory to save the file in.
    file_type (str): The type of file (e.g., 'code', 'doc').

    Returns:
    None
    """
    os.makedirs(os.path.join(directory, subdir), exist_ok=True)
    file_path = os.path.join(directory, subdir, f"{file_type}_embedded.json")
    with open(file_path, "w") as file:
        json.dump(data, file)


def write_file(file_path, content):
    """
    Write content to a file.

    Parameters:
    file_path (str): The path to the file.
    content (str): The content to write to the file.

    Returns:
    None
    """
    with open(file_path, "w") as file:
        file.write(content)

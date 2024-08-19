# Import necessary modules
import openai
import os
import sys
import time
import re
import ast
from constants import DEFAULT_DIRECTORY, DEFAULT_MODEL, DEFAULT_MAX_TOKENS
from utils import clean_dir, write_file

from dotenv import load_dotenv

# Initialize OpenAI and GitHub API keys
openai.api_key = os.getenv("OPENAI_API_KEY")


# Initialize a session with OpenAI's chat models
def chat_with_gpt3(systemprompt, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemprompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )
    return response["choices"][0]["message"]["content"]


def save_to_local_directory(repo_name, functions):
    # Check if the directory already exists
    if not os.path.exists(repo_name):
        # If not, create it
        os.makedirs(repo_name)

    # Create a new file in the directory to hold all the functions
    file_path = os.path.join(repo_name, "functions.py")
    with open(file_path, "w") as f:
        # Write all the functions to the file
        for function in functions:
            f.write(function)
            f.write("\n\n")


def old_save_to_local_directory(repo_name, functions):
    # Check if the directory already exists
    if not os.path.exists(repo_name):
        # If not, create it
        os.makedirs(repo_name)
    # Create a new file in the directory for each function
    for i, function in enumerate(functions):
        with open(f"{repo_name}/function_{i+1}.py", "w") as f:
            f.write(function)


def generate_filepaths(prompt):
    systemprompt = f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    When given their intent, create a complete, exhaustive list of filepaths that the user would write to make the program.
    
    only list the filepaths you would write, and return them as a python array of strings. 
    do not add any other explanation, only return a python array of strings."""
    result = chat_with_gpt3(systemprompt, prompt)
    print(result)
    return result


def generate_shared_dependencies(prompt, filepaths):
    systemprompt = f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
                
            In response to the user's prompt:

            ---
            the app is: {prompt}
            ---
            
            the files we have decided to generate are: {filepaths}

            Now that we have a list of files, we need to understand what dependencies they share.
            Please name and briefly describe what is shared between the files we are generating, including exported variables, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
            Exclusively focus on the names of the shared dependencies, and do not add any other explanation.
    """
    result = chat_with_gpt3(systemprompt, prompt)
    print(result)
    return result


def generate_file(filename, filepaths=None, shared_dependencies=None, prompt=None):
    # call openai api with this prompt
    systemprompt = f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    the app is: {prompt}

    the files we have decided to generate are: {filepaths}

    the shared dependencies (like filenames and variable names) we have decided on are: {shared_dependencies}
    
    only write valid code for the given filepath and file type, and return only the code.
    do not add any other explanation, only return valid code for that file type.
    """
    userprompt = f"""
    We have broken up the program into per-file generation. 
    Now your job is to generate only the code for the file {filename}. 
    Make sure to have consistent filenames if you reference other files we are also generating.
    
    Remember that you must obey 3 things: 
       - you are generating code for the file {filename}
       - do not stray from the names of the files and the shared dependencies we have decided on
       - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be valid code. Do not include code fences in your response, for example
    
    Bad response:
    ```javascript 
    console.log("hello world")
    ```
    
    Good response:
    console.log("hello world")
    
    Begin generating the code now.

    """
    filecode = chat_with_gpt3(systemprompt, userprompt)

    return filename, filecode


# Main function
def main(prompt, directory=DEFAULT_DIRECTORY, model=DEFAULT_MODEL, file=None):
    # Get the project objective from the user
    if prompt.endswith(".md"):
        with open(prompt, "r") as f:
            prompt = f.read()
    print("Hello, I am your local AI developer! You said you wanted:")
    print("\033[92m" + prompt + "\033[0m")
    # Get the repo name from the user
    repo_name = input("Enter the name for the new directory: ")
    directory = os.path.join(directory, repo_name)
    filepaths = generate_filepaths(prompt)
    list_actual = []
    try:
        list_actual = ast.literal_eval(filepaths)
        shared_dependencies = None
        if os.path.exists("shared_dependencies.md"):
            with open("shared_dependencies.md", "r") as f:
                shared_dependencies = f.read()

        if file is not None:
            print("File", file)
            filename, filecode = generate_file(
                file,
                model=model,
                filepaths=filepaths,
                shared_dependencies=shared_dependencies,
                prompt=prompt,
            )
            write_file(filename, filecode, directory)
        else:
            clean_dir(directory)

            shared_dependencies = generate_shared_dependencies(prompt, filepaths)
            write_file("shared_dependencies.md", shared_dependencies, directory)

            for filename in list_actual:
                filename, filecode = generate_file(
                    filename,
                    filepaths=filepaths,
                    shared_dependencies=shared_dependencies,
                    prompt=prompt,
                )
                write_file(filename, filecode, directory)
    except ValueError:
        print("Failed to parse result")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        if not os.path.exists("prompt.md"):
            print("Please provide a prompt file or a prompt string")
            sys.exit(1)
        else:
            prompt = "prompt.md"

    else:
        prompt = sys.argv[1]

    directory = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DIRECTORY
    file = sys.argv[3] if len(sys.argv) > 3 else None
    main(prompt, directory, file)

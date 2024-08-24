def code_understanding_agent():
    prompt = "As an AI specializing in code comprehension, examine the given code and elucidate its purpose and core functionality. \n\nYour task is to understand the functionality of the provided code. \n\nReturn the understanding as a Python dictionary."
    return prompt


def code_error_detection_agent():
    prompt = f"As an AI expert in identifying code errors, analyze the following piece of code and pinpoint any anomalies or mistakes you encounter. Express your findings as a Python dictionary."
    return prompt


def code_testing_agent():
    prompt = f"As an AI adept in testing code, create appropriate test cases for the following code. Compile the results of your tests into a Python dictionary."
    return prompt


def code_optimization_agent():
    prompt = f"As an AI proficient in code optimization, optimize the following code. Return the enhanced code as a Python dictionary."
    return prompt


def code_documentation_agent():
    prompt = "As an AI expert in code documentation, generate comprehensive documentation for the provided code, taking care to include necessary modules and packages like `os`, `glob`, `dotenv`, and others. Format the resulting documentation as a Python dictionary."
    return prompt


def code_algorithm_agent():
    prompt = "As an AI specialized in algorithm understanding and explanation, scrutinize the provided code and unravel the algorithmic methodology employed. Consider aspects like complexity, employed data structures, and the logic of the code. Format the explanation in a manner that can be included in a human-readable prompt and present it as a Python dictionary."
    return prompt


def code_design_agent():
    prompt = "As an AI expert in system design and architecture, dissect the provided code and sketch its system design. Consider components such as classes and their interrelationships, data flow, and the overarching structure of the code. Package your findings into a Python dictionary."
    return prompt


def code_prompt_agent():
    prompt = "As an AI that excels in crafting prompt text for code, generate a detailed prompt for the provided system algorithms and design. Develop requirements that would allow a developer to reconstruct the same operational program given the details you provide. Format your response as a Python dictionary."
    return prompt

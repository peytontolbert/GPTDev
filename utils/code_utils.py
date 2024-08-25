import re


def get_function_name(code):
    """
    Extract the function name from a piece of code.

    Parameters:
    code (str): The code containing the function definition.

    Returns:
    str: The name of the function.
    """
    match = re.search(r"def\s+(\w+)\s*\(", code)
    if match:
        return match.group(1)
    return None


def get_until_no_space(lines, start_index):
    """
    Get lines of code until a line with no leading spaces is found.

    Parameters:
    lines (list): List of lines of code.
    start_index (int): The index to start from.

    Returns:
    str: The concatenated lines of code.
    """
    code_lines = []
    for i in range(start_index, len(lines)):
        if lines[i].strip() == "":
            continue
        if not lines[i].startswith(" "):
            break
        code_lines.append(lines[i])
    return "\n".join(code_lines)


def get_until_no_space(all_lines, i) -> str:
    """
    Get all lines until a line outside the function definition is found.
    """
    ret = [all_lines[i]]
    for j in range(i + 1, i + 10000):
        if j < len(all_lines):
            if len(all_lines[j]) == 0 or all_lines[j][0] in [" ", "\t", ")"]:
                ret.append(all_lines[j])
            else:
                break
    return "\n".join(ret)

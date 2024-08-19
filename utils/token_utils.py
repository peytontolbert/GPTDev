import tiktoken


def num_tokens_from_string(string, encoding_name="gpt2"):
    """
    Returns the number of tokens in a text string.

    Parameters:
    string (str): The text string to tokenize.
    encoding_name (str): The name of the encoding to use (default is 'gpt2').

    Returns:
    int: The number of tokens in the string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def truncate_text_tokens(text, max_tokens, encoding_name="gpt2"):
    """
    Truncate a text string to a maximum number of tokens.

    Parameters:
    text (str): The text string to truncate.
    max_tokens (int): The maximum number of tokens.
    encoding_name (str): The name of the encoding to use (default is 'gpt2').

    Returns:
    str: The truncated text string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    truncated_tokens = tokens[:max_tokens]
    truncated_text = encoding.decode(truncated_tokens)
    return truncated_text


def len_safe_get_embedding(text, model, max_tokens, encoding_name="gpt2"):
    """
    Get the embedding of a text string, ensuring it does not exceed the maximum number of tokens.

    Parameters:
    text (str): The text string to embed.
    model (str): The model to use for embedding.
    max_tokens (int): The maximum number of tokens.
    encoding_name (str): The name of the encoding to use (default is 'gpt2').

    Returns:
    list: The embedding of the text string.
    """
    truncated_text = truncate_text_tokens(text, max_tokens, encoding_name)
    embedding = get_embedding(truncated_text, model)
    return embedding

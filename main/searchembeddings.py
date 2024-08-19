from openai.embeddings_utils import cosine_similarity, get_embedding
import pandas as pd
import openai
import numpy as np
import os
from dotenv import load_dotenv

# Initialize OpenAI and GitHub API keys
openai.api_key = os.getenv("OPENAI_API_KEY")


def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
    embedding = get_embedding(code_query, engine="text-embedding-ada-002")
    df["similarities"] = df.code_embedding.apply(
        lambda x: cosine_similarity(x, embedding)
    )

    res = df.sort_values("similarities", ascending=False).head(n)
    if pprint:
        for r in res.iterrows():
            print(
                r[1].filepath
                + ":"
                + r[1].function_name
                + " score="
                + str(round(r[1].similarities, 3))
            )
            print("\n".join(r[1].code.split("\n")[:n_lines]))
            print("-" * 70)
        return res


df = pd.read_csv("functions2.csv")
df["code_embedding"] = df.code_embedding.apply(eval).apply(np.array)
res = search_functions(df, "get_filenames", n=3)

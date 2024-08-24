from base_agent import Agent
from src.codesearch import get_embedding
import pandas as pd

class CodeEmbeddingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def embed_code(self, functions):
        df = pd.DataFrame(functions)
        df["code_embedding"] = df["code"].apply(
            lambda x: get_embedding(x, engine="text-embedding-ada-002")
        )
        return df

    def execute(self, input_data):
        embedded_code = self.embed_code(input_data)
        embedded_code.to_csv('embedded_code.csv', index=True)


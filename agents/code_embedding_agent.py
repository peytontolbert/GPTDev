from agents.base_agent import Agent
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
class CodeEmbeddingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def embed_code(self, functions):
        df = pd.DataFrame(functions)
        df["code_embedding"] = df["code"].apply(
            lambda x: self.get_embedding(x, engine="text-embedding-ada-002")
        )
        return df

    def execute(self, input_data):
        embedded_code = self.embed_code(input_data)
        embedded_code.to_csv('embedded_code.csv', index=True)


    def get_embedding(self, text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding

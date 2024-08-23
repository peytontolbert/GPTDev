class Agent:
    def __init__(self, name):
        self.name = name
    
    def execute(self, input_data):
        raise NotImplementedError("Each agent must implement the execute method.")
    
    def generate_prompt(self):
        raise NotImplementedError("Each agent must implement the generate_prompt method.")
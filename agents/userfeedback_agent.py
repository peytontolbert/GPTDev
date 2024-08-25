
from agents.base_agent import Agent
"""
User Feedback Agent: Collects and analyzes user feedback to inform development priorities.
"""
class UserFeedbackAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        analyzed_feedback = self.analyze_feedback(input_data)
        self.save_to_file('analyzed_feedback.txt', analyzed_feedback)
    
    def analyze_feedback(self, feedback_data):
        prompt = self.generate_prompt(feedback_data)
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def generate_prompt(self, input_data):
        return f"""You are a helpful AI assistant that can analyze user feedback and identify potential improvements and prioritize them. 
        
        Analyze the following user feedback and provide:
        1. A summary of the feedback.
        2. Identify potential improvements based on the feedback.
        3. Prioritize these improvements based on their urgency and impact. 
        
        User Feedback: {input_data}"""
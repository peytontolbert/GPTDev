import time
import psutil

class PerformanceMonitoringAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        start_time = time.time()
        start_cpu = psutil.cpu_percent(interval=None)
        start_memory = psutil.virtual_memory().used

        try:
            result = self.perform_task(input_data)
        except Exception as e:
            self.log(f"Error: {str(e)}")
            result = None

        end_time = time.time()
        end_cpu = psutil.cpu_percent(interval=None)
        end_memory = psutil.virtual_memory().used

        self.log_performance(start_time, end_time, start_cpu, end_cpu, start_memory, end_memory)
        return result

    def perform_task(self, input_data):
        # Implement the specific task logic here
        return f"Task performed with input: {input_data}"

    def log_performance(self, start_time, end_time, start_cpu, end_cpu, start_memory, end_memory):
        execution_time = end_time - start_time
        cpu_usage = end_cpu - start_cpu
        memory_usage = end_memory - start_memory

        self.log(f"Execution Time: {execution_time} seconds")
        self.log(f"CPU Usage: {cpu_usage}%")
        self.log(f"Memory Usage: {memory_usage} bytes")

    def generate_prompt(self, input_data):
        # Implement the prompt generation logic here
        return f"Monitor the performance of the following input: {input_data}"

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}


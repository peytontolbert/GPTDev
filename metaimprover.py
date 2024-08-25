import os
from gptbuilder_improver import GPTBuilderImprover

class MetaImprover:
    def __init__(self, target_file: str, iterations: int = 3):
        self.target_file = target_file
        self.iterations = iterations
        self.improver = GPTBuilderImprover()

    def run(self):
        print(f"Starting meta-improvement process for {self.target_file}")
        current_file = self.target_file

        for i in range(self.iterations):
            print(f"\nMeta-iteration {i+1}/{self.iterations}")
            
            # Load and improve the current version
            self.improver.load_original_code(current_file)
            improved_code = self.improver.improve_builder(iterations=1)
            
            # Save the improved version with a new name
            new_file = f"improved_{os.path.basename(current_file)}"
            self.improver.save_improved_code(new_file)
            
            print(f"Improved version saved as {new_file}")
            current_file = new_file

        print("\nMeta-improvement process completed.")
        print(f"Final improved version: {current_file}")

if __name__ == "__main__":
    meta_improver = MetaImprover("gptbuilder_improver.py", iterations=3)
    meta_improver.run()
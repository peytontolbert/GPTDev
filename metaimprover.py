import os
from gptbuilder_improver import GPTBuilderImprover
import logging

class MetaImprover:
    def __init__(self, target_file: str, max_iterations: int = 10, quality_threshold: float = 0.8):
        self.target_file = target_file
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.improver = GPTBuilderImprover()
        self.iteration_count = 0
        self.previous_quality = 0.0

    def run(self):
        print(f"Starting meta-improvement process for {self.target_file}")
        current_file = self.target_file

        for i in range(self.max_iterations):
            self.iteration_count += 1
            print(f"\nMeta-iteration {self.iteration_count}/{self.max_iterations}")
            
            # Load and improve the current version
            self.improver.load_original_code(current_file)
            improved_code = self.improver.improve_builder(iterations=1)
            
            # Save the improved version with a new name
            new_file = f"improved_{i}_{os.path.basename(current_file)}"
            self.improver.save_improved_code(new_file)
            
            print(f"Improved version saved as {new_file}")
            current_file = new_file
            
            # Assess the quality of the improvement
            quality = self._assess_quality(improved_code)
            print(f"Iteration {self.iteration_count} quality score: {quality:.2f}")
            
            if quality < self.quality_threshold:
                print("Improvement quality is below threshold, stopping meta-improvement process.")
                break
            
            # Re-evaluate and possibly re-iterate based on new insights
            if quality > self.previous_quality:
                self.previous_quality = quality
                print("Quality has improved, continuing iterations.")
            else:
                print("No significant quality improvement, pushing for transformational changes.")
                # Trigger transformational improvements
                improved_code = self._transformational_improvements(improved_code)
                self.previous_quality = self._assess_quality(improved_code)
                if self.previous_quality < self.quality_threshold:
                    print("Transformational changes did not improve quality significantly. Stopping.")
                    break
                self.improver.save_improved_code(new_file)

        print("\nMeta-improvement process completed.")
        print(f"Final improved version: {current_file}")

    def _assess_quality(self, improved_code: str) -> float:
        evaluation_prompt = f"""
        Evaluate the following Python code based on the following criteria:
        1. Code structure and organization
        2. Efficiency and performance
        3. Modularity and extensibility
        4. Error handling and robustness
        5. Documentation and readability

        Provide a quality score from 0 to 1, where 1 is the highest quality. Consider all the criteria in your assessment.

        Improved Code:
        {improved_code}
        """

        system_prompt = "You are an expert Python developer and code reviewer."
        response = self.improver.gpt.chat_with_ollama(system_prompt, evaluation_prompt)
        
        try:
            quality_score = float(response.strip())
            logging.info(f"Quality score assessed by GPT: {quality_score}")
            return quality_score
        except ValueError:
            logging.error("Error: GPT response is not a valid number. Assuming default quality score of 0.5.")
            return 0.5  # Default to a mid-range score if there's an issue

    def _transformational_improvements(self, code: str) -> str:
        """
        Apply transformational improvements to the script by challenging the LLM to think beyond incremental changes.
        """
        transformational_prompt = f"""
        The current version of this script has been optimized and improved incrementally. Now, consider how this script could evolve into the ultimate version of itself. 
        Think beyond small improvements and consider transformational changes that could greatly enhance its capabilities, scalability, and usability.

        Current Code:
        {code}

        Some ideas to consider:
        1. New features or functionalities that could be added.
        2. Significant changes to the architecture or design.
        3. Integration with other tools or technologies.
        4. Advanced error handling or self-improvement mechanisms.
        5. Enhancements that make the script future-proof.

        Provide your suggestions and the corresponding code changes.
        """
        system_prompt = "You are an AI and Python expert tasked with designing the ultimate version of this script."
        response = self.improver.gpt.chat_with_ollama(system_prompt, transformational_prompt)
        
        return response.strip()

if __name__ == "__main__":
    meta_improver = MetaImprover("gptbuilder_improver.py", max_iterations=10, quality_threshold=0.85)
    meta_improver.run()
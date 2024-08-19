import unittest
from unittest.mock import patch
from ai_coder.main.start_largecode import CodebaseGenerator


class TestCodebaseGenerator(unittest.TestCase):
    def setUp(self):
        self.prompt = "Create a simple calculator program."
        self.directory = "./test_directory"
        self.generator = CodebaseGenerator(self.prompt, self.directory)

    @patch("builtins.input", side_effect=["no", "q"])
    def test_clarify_prompt(self, mock_input):
        result = self.generator.clarify_prompt()
        self.assertIn("Create a simple calculator program.no", result)

    def test_parse_response(self):
        # Test the parse_response function
        pass

    def test_design_program_structure(self):
        # Test the design_program_structure function
        pass

    def test_generate_file_paths(self):
        # Test the generate_file_paths function
        pass

    def test_generate_shared_dependencies(self):
        # Test the generate_shared_dependencies function
        pass

    def test_generate_code_for_each_file(self):
        # Test the generate_code_for_each_file function
        pass

    def test_AI_generate_code_and_tests(self):
        # Test the AI_generate_code_and_tests function
        pass

    def test_write_code_and_tests(self):
        # Test the write_code_and_tests function
        pass

    def test_write_files_to_directory(self):
        # Test the write_files_to_directory function
        pass

    def test_debug_generated_code(self):
        # Test the debug_generated_code function
        pass


if __name__ == "__main__":
    unittest.main()

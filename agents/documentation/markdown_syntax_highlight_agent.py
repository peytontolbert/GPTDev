
from agents.base_agent import Agent
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import concurrent.futures

class MarkdownSyntaxHighlighterAgent(Agent):
    def __init__(self, name="MarkdownSyntaxHighlighter"):
        super().__init__(name)
        self.code_block_pattern = re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        highlighted_markdown = self.highlight_markdown(input_data)
        return highlighted_markdown

    def generate_prompt(self, input_data):
        return f"Highlight the syntax in the following markdown:\n\n{input_data}"

    def highlight_markdown(self, markdown):
        def highlight_block(match):
            lang, code = match.groups()
            if lang is None:
                lang = 'text'
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ValueError:
                lexer = get_lexer_by_name('text', stripall=True)
            formatter = HtmlFormatter(style='monokai')
            highlighted = highlight(code, lexer, formatter)
            return f'```{lang}\n{highlighted}\n```'

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Find all code blocks
            code_blocks = list(self.code_block_pattern.finditer(markdown))
            
            # Highlight code blocks in parallel
            highlighted_blocks = list(executor.map(highlight_block, code_blocks))

        # Replace original code blocks with highlighted versions
        for original, highlighted in zip(code_blocks, highlighted_blocks):
            markdown = markdown.replace(original.group(), highlighted)

        return markdown

    def parse_response(self, response):
        # No need to parse the response in this case
        return response

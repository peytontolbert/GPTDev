import os

class UtilityFunctions:
    @staticmethod
    def save_to_file(path, content):
        with open(path, 'w') as f:
            f.write(content)


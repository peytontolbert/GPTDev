
import os
import json

class Persona:
    def __init__(self, name, background, interests):
        self.name = name
        self.background = background
        self.interests = interests
        self.history = []
        self.file_system = {}

    def create_file(self, file_name, content):
        self.file_system[file_name] = content
        self.history.append(f"Created file {file_name}")

    def view_file(self, file_name):
        return self.file_system.get(file_name, "File not found")

    def list_files(self):
        return list(self.file_system.keys())

    def interact_with_discord(self, message):
        # Simulate interaction with Discord
        self.history.append(f"Interacted with Discord: {message}")

    def save_state(self):
        state = {
            "name": self.name,
            "background": self.background,
            "interests": self.interests,
            "history": self.history,
            "file_system": self.file_system
        }
        with open(f"{self.name}_state.json", "w") as f:
            json.dump(state, f)

    def load_state(self):
        try:
            with open(f"{self.name}_state.json", "r") as f:
                state = json.load(f)
                self.name = state["name"]
                self.background = state["background"]
                self.interests = state["interests"]
                self.history = state["history"]
                self.file_system = state["file_system"]
        except FileNotFoundError:
            pass

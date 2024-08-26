from datetime import datetime

class AgentVersion:
    def __init__(self, code, version=1, changes="Initial version"):
        self.code = code
        self.version = version
        self.changes = changes
        self.timestamp = datetime.now().isoformat()

class AgentVersionControl:
    def __init__(self):
        self.versions = {}

    def add_version(self, agent_name, code, changes):
        if agent_name not in self.versions:
            self.versions[agent_name] = []
        new_version = len(self.versions[agent_name]) + 1
        self.versions[agent_name].append(AgentVersion(code, new_version, changes))
        return new_version

    def get_latest_version(self, agent_name):
        return self.versions[agent_name][-1] if agent_name in self.versions else None

    def rollback(self, agent_name, version):
        if agent_name in self.versions and 1 <= version <= len(self.versions[agent_name]):
            return self.versions[agent_name][version - 1].code
        return None

    def get_changelog(self, agent_name):
        if agent_name not in self.versions:
            return ""
        changelog = f"# Changelog for {agent_name}\n\n"
        for version in reversed(self.versions[agent_name]):
            changelog += f"## Version {version.version} - {version.timestamp}\n"
            changelog += f"{version.changes}\n\n"
        return changelog


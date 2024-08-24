from agents.bugtracking_agent import BugTrackingAgent

# Initialize agent
bug_tracking_agent = BugTrackingAgent('BugTrackingAgent')

# Define the main function
def main(project_path):
    # Step 1: Track bugs
    bug_tracking_agent.track_bugs(project_path)
    
    # Step 2: Generate bug report
    bug_tracking_agent.generate_bug_report()

# Example usage
if __name__ == '__main__':
    example_project_path = './path_to_project'
    main(example_project_path)


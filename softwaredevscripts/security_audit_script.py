from agents.securityaudit_agent import SecurityAuditAgent

project_path = "./path_to_project"

audit_agent = SecurityAuditAgent("Security Audit Agent")
audit_agent.perform_security_audit(project_path)
audit_agent.generate_audit_report()

from datetime import datetime

audit_log = []

def log_action(case_id, user_role, action):
    audit_log.append({
        "case_id": case_id,
        "user_role": user_role,
        "action": action,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def get_audit(case_id):
    return [a for a in audit_log if a["case_id"] == case_id]

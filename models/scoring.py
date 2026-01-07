import pandas as pd

def compute_recovery_score(row):
    score = 1.0

    # 1. Ageing penalty (non-linear: old cases decay faster)
    if row["ageing_days"] > 120:
        score -= 0.4
    elif row["ageing_days"] > 60:
        score -= 0.25
    else:
        score -= row["ageing_days"] / 300

    # 2. Business sensitivity
    if row["business_type"] == "Enterprise":
        score += 0.15
    elif row["business_type"] == "Small":
        score -= 0.05

    # 3. Dispute blocker
    if row["dispute_status"] == "Open":
        score -= 0.5
    elif row["dispute_status"] == "Resolved":
        score += 0.1

    # 4. DCA responsiveness (this is key for accountability)
    if row["last_dca_update_days"] > 7:
        score -= 0.3
    elif row["last_dca_update_days"] > 3:
        score -= 0.15

    # 5. SLA breach penalty
    if row["sla_status"] == "BREACHED":
        score -= 0.2

    return round(max(0, min(score, 1)), 2)



def next_best_action(row):
    if row["dispute_status"] == "Open":
        return "Resolve Dispute (Block Collections)"

    if row["invoice_amount"] > 250000 and row["ageing_days"] > 90:
        return "Escalate to Legal"

    if row["last_dca_update_days"] > 7:
        return "Auto-Nudge DCA (SLA Breach)"

    if row["recovery_score"] > 0.75:
        return "High Probability – Aggressive Follow-up"

    if row["recovery_score"] < 0.3:
        return "Low Probability – Review / Deprioritize"

    return "Standard Follow-up"



def apply_scoring(df):
    df["recovery_score"] = df.apply(compute_recovery_score, axis=1)
    df["expected_recovery"] = df["invoice_amount"] * df["recovery_score"]
    df["ai_next_action"] = df.apply(next_best_action, axis=1)
    return df

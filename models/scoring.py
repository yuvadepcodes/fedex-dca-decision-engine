import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==================== ADVANCED ML SCORING ====================

def compute_recovery_score(row):
    """
    Multi-factor recovery prediction model using weighted ML approach
    Factors: Ageing, Business Type, Dispute, DCA Performance, Payment History
    """
    score = 0.5  # Base score
    
    # 1. AGEING DECAY (exponential decay - older cases lose value faster)
    ageing_days = row["ageing_days"]
    ageing_factor = np.exp(-0.015 * ageing_days) * 0.35
    score += ageing_factor
    
    # 2. BUSINESS SEGMENT MULTIPLIER (enterprise vs SMB)
    business_multiplier = {
        "Enterprise": 1.25,
        "Large": 1.10,
        "Medium": 0.95,
        "Small": 0.70
    }
    segment_boost = business_multiplier.get(row.get("business_type", "Medium"), 0.95) - 1
    score += segment_boost * 0.15
    
    # 3. DISPUTE IMPACT (critical blocker)
    if row.get("dispute_status") == "Open":
        score -= 0.40
    elif row.get("dispute_status") == "Resolved":
        score += 0.10
    elif row.get("dispute_status") == "Pending_Resolution":
        score -= 0.20
    
    # 4. DCA RESPONSIVENESS (accountability metric)
    last_update = row.get("last_dca_update_days", 30)
    responsiveness = max(0, 1 - (last_update / 30)) * 0.20
    score += responsiveness
    
    if last_update > 14:
        score -= 0.15
    
    # 5. PAYMENT HISTORY (if available)
    if "payment_history" in row and row["payment_history"] == "Good":
        score += 0.15
    elif "payment_history" in row and row["payment_history"] == "Bad":
        score -= 0.20
    
    # 6. SLA BREACH PENALTY
    if row.get("sla_status") == "BREACHED":
        score -= 0.25
    elif row.get("sla_status") == "AT_RISK":
        score -= 0.10
    
    # 7. INVOICE AMOUNT NORMALIZATION (larger amounts = higher urgency)
    invoice_normalized = min(row.get("invoice_amount", 100000) / 500000, 1.0)
    score += invoice_normalized * 0.10
    
    # Normalize to 0-1 range with sigmoid-like scaling
    final_score = max(0, min(score, 1.0))
    return round(final_score, 3)


def compute_recovery_probability(row):
    """Estimates actual recovery probability (0-100%)"""
    base_probability = compute_recovery_score(row) * 100
    
    # Adjust based on ageing
    if row["ageing_days"] > 180:
        base_probability *= 0.6
    elif row["ageing_days"] > 120:
        base_probability *= 0.75
    elif row["ageing_days"] > 60:
        base_probability *= 0.9
    
    return round(base_probability, 1)


def compute_priority_score(row):
    """
    Priority = Recovery Probability × Invoice Amount × Urgency Factor
    Higher score = Higher priority for DCA allocation
    """
    recovery_prob = compute_recovery_score(row)
    invoice_amount = row.get("invoice_amount", 100000)
    
    # Urgency increases with ageing
    urgency = 1 + (row["ageing_days"] / 180)  # 1.0 to 2.0+ factor
    
    priority = recovery_prob * invoice_amount * urgency
    return round(priority, 0)


def compute_dca_sla_deadline(case_date, case_type="standard"):
    """
    SLA deadline calculator based on case type
    standard: 30 days, high_value: 15 days, escalated: 7 days
    """
    sla_days = {
        "standard": 30,
        "high_value": 15,
        "escalated": 7,
        "legal": 3
    }
    return case_date + timedelta(days=sla_days.get(case_type, 30))


def next_best_action(row):
    """
    AI-driven action recommendation engine
    """
    # BLOCKER CHECKS
    if row.get("dispute_status") == "Open":
        return "🛑 Resolve Dispute First"
    
    if row.get("last_dca_update_days", 0) > 14:
        return "⚠️ Auto-Escalate: DCA Unresponsive"
    
    if row.get("sla_status") == "BREACHED":
        return "🚨 CRITICAL: SLA Breach - Manager Review"
    
    # RECOVERY PROBABILITY BASED ACTIONS
    recovery_prob = compute_recovery_probability(row)
    invoice_amount = row.get("invoice_amount", 0)
    ageing_days = row.get("ageing_days", 0)
    
    # High-value escalations
    if invoice_amount > 500000 and ageing_days > 90:
        return "👨‍⚖️ Escalate to Legal Team"
    
    if invoice_amount > 250000 and recovery_prob < 30:
        return "📋 Review for Settlement / Write-off"
    
    # Recovery probability driven actions
    if recovery_prob > 80:
        return "💪 Aggressive Follow-up - High Success Rate"
    elif recovery_prob > 60:
        return "📞 Priority Follow-up Campaign"
    elif recovery_prob > 40:
        return "✉️ Standard Collection Process"
    elif recovery_prob > 20:
        return "⏳ Nurture Phase - Periodic Contact"
    else:
        return "📊 Low Probability - Review Strategy"


def calculate_expected_recovery(row):
    """Expected recovery amount = Invoice × Recovery Probability"""
    recovery_prob = compute_recovery_probability(row) / 100
    return round(row.get("invoice_amount", 0) * recovery_prob, 2)


def compute_churn_risk(row):
    """
    Churn Risk Prediction: Probability that customer WON'T pay
    High churn risk = customer likely to default/abandon
    Factors: Aging, dispute status, DCA inactivity, business type
    Returns: 0-100 (0=low risk, 100=high risk)
    """
    churn_score = 0
    
    # AGING FACTOR (critical) - older cases have higher churn
    ageing = row.get("ageing_days", 0)
    if ageing > 180:
        churn_score += 40
    elif ageing > 120:
        churn_score += 30
    elif ageing > 60:
        churn_score += 15
    
    # DISPUTE STATUS (major predictor)
    if row.get("dispute_status") == "Open":
        churn_score += 35
    elif row.get("dispute_status") == "Pending_Resolution":
        churn_score += 15
    
    # DCA INACTIVITY (indicates customer disengagement)
    last_update = row.get("last_dca_update_days", 0)
    if last_update > 21:
        churn_score += 25
    elif last_update > 14:
        churn_score += 15
    
    # BUSINESS TYPE (SMB higher churn than Enterprise)
    business_type = row.get("business_type", "Medium")
    if business_type == "Small":
        churn_score += 20
    elif business_type == "Medium":
        churn_score += 10
    
    # SLA STATUS
    if row.get("sla_status") == "BREACHED":
        churn_score += 20
    
    # NORMALIZE TO 0-100
    churn_risk = min(max(churn_score, 0), 100)
    return round(churn_risk, 1)


def compute_optimal_followup_timing(row):
    """
    Optimal Follow-up Timing Recommendation
    Based on aging pattern, recovery probability, and DCA activity
    Returns: Days until optimal follow-up
    """
    recovery_prob = compute_recovery_probability(row)
    ageing = row.get("ageing_days", 0)
    last_update = row.get("last_dca_update_days", 0)
    
    # High probability cases: follow up faster
    if recovery_prob > 75:
        optimal_days = 3  # Aggressive 3-day cycle
    elif recovery_prob > 60:
        optimal_days = 5  # Medium-aggressive
    elif recovery_prob > 40:
        optimal_days = 7  # Weekly follow-ups
    elif recovery_prob > 20:
        optimal_days = 14  # Bi-weekly for low probability
    else:
        optimal_days = 30  # Monthly for very low probability
    
    # ADJUST for aging
    if ageing > 150:
        optimal_days = max(1, optimal_days - 2)  # Increase frequency
    
    # If DCA hasn't updated in a while, force immediate action
    if last_update > 14:
        optimal_days = 1
    
    return optimal_days


def get_predictive_insights(row):
    """
    Generate comprehensive predictive insights for case
    Returns: Dict with predictions and recommendations
    """
    recovery_prob = compute_recovery_probability(row)
    churn_risk = compute_churn_risk(row)
    followup_timing = compute_optimal_followup_timing(row)
    
    # Determine insight category
    if recovery_prob > 70 and churn_risk < 30:
        insight_type = "🟢 HIGH CONFIDENCE RECOVERY"
        recommendation = "Prioritize this case. High recovery probability with low churn risk."
    elif recovery_prob > 50 and churn_risk < 50:
        insight_type = "🟡 MODERATE OPPORTUNITY"
        recommendation = "Steady engagement recommended. Monitor for signs of default."
    elif churn_risk > 70:
        insight_type = "🔴 HIGH CHURN RISK"
        recommendation = "Immediate action required. Customer likely to default soon. Consider settlement."
    elif recovery_prob < 30:
        insight_type = "⚠️ LOW RECOVERY POTENTIAL"
        recommendation = "Consider write-off or settlement. High collection cost vs low recovery."
    else:
        insight_type = "⏳ NURTURE PHASE"
        recommendation = "Maintain periodic contact. Build relationship for eventual recovery."
    
    return {
        "recovery_probability": recovery_prob,
        "churn_risk": churn_risk,
        "optimal_followup_days": followup_timing,
        "insight_type": insight_type,
        "recommendation": recommendation
    }


def compute_dca_efficiency_score(dca_cases_df):
    """
    Evaluate individual DCA's efficiency
    Higher = More efficient at collecting
    """
    if len(dca_cases_df) == 0:
        return 0
    
    # Metrics
    avg_recovery_prob = dca_cases_df["recovery_probability"].mean()
    avg_responsiveness = 100 - dca_cases_df["last_dca_update_days"].mean()
    resolved_cases = len(dca_cases_df[dca_cases_df["dispute_status"].isin(["Resolved", "None"])])
    total_cases = len(dca_cases_df)
    resolution_rate = (resolved_cases / total_cases * 100) if total_cases > 0 else 0
    
    # Weighted score
    efficiency = (avg_recovery_prob * 0.4 + 
                  (avg_responsiveness / 100 * 100) * 0.3 + 
                  resolution_rate * 0.3)
    
    return round(efficiency, 1)


def risk_assessment(row):
    """
    Risk categorization for portfolio management
    HIGH: >120 days ageing + open disputes
    MEDIUM: 60-120 days
    LOW: <60 days
    """
    ageing = row.get("ageing_days", 0)
    
    if ageing > 120 and row.get("dispute_status") == "Open":
        return "CRITICAL"
    elif ageing > 120:
        return "HIGH"
    elif ageing > 60:
        return "MEDIUM"
    else:
        return "LOW"


def apply_scoring(df):
    """Apply all ML scoring models to dataframe"""
    df["recovery_score"] = df.apply(compute_recovery_score, axis=1)
    df["recovery_probability"] = df.apply(compute_recovery_probability, axis=1)
    df["priority_score"] = df.apply(compute_priority_score, axis=1)
    df["expected_recovery"] = df.apply(calculate_expected_recovery, axis=1)
    df["churn_risk"] = df.apply(compute_churn_risk, axis=1)
    df["optimal_followup_days"] = df.apply(compute_optimal_followup_timing, axis=1)
    df["ai_next_action"] = df.apply(next_best_action, axis=1)
    df["risk_level"] = df.apply(risk_assessment, axis=1)
    return df

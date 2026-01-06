import numpy as np
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("model/recovery_model.pkl")
le_customer = joblib.load("model/customer_encoder.pkl")
le_region = joblib.load("model/region_encoder.pkl")

def calculate_priority(row):
    # Normalize values
    norm_amount = row["overdue_amount"] / 500000
    norm_days = row["days_overdue"] / 365
    norm_escalations = row["previous_escalations"] / 3

    priority_score = (
        0.4 * row["recovery_probability"] +
        0.3 * norm_amount +
        0.2 * norm_days -
        0.1 * norm_escalations
    )

    return round(priority_score, 2)

def confidence_level(row):
    if row["days_overdue"] < 30:
        return "LOW"
    elif row["days_overdue"] < 90:
        return "MEDIUM"
    else:
        return "HIGH"

def recommend_dca(priority_score):
    if priority_score >= 0.75:
        return "Top Performing DCA"
    elif priority_score >= 0.5:
        return "Mid Tier DCA"
    else:
        return "Low Cost DCA"

def run_prioritization(df):
    df = df.copy()

    # Encode categorical columns
    df["customer_type"] = le_customer.transform(df["customer_type"])
    df["region"] = le_region.transform(df["region"])

    feature_cols = [
        "overdue_amount",
        "days_overdue",
        "customer_type",
        "region",
        "past_recovery_rate",
        "dca_experience_score",
        "previous_escalations"
    ]

    probs = model.predict_proba(df[feature_cols])[:, 1]
    df["recovery_probability"] = probs.round(2)

    df["priority_score"] = df.apply(calculate_priority, axis=1)
    df["confidence_level"] = df.apply(confidence_level, axis=1)
    df["recommended_dca"] = df["priority_score"].apply(recommend_dca)

    return df

import pandas as pd
import numpy as np

np.random.seed(42)

NUM_CASES = 500

case_id = [f"CASE_{1000+i}" for i in range(NUM_CASES)]

overdue_amount = np.random.randint(5000, 500000, NUM_CASES)
days_overdue = np.random.randint(1, 365, NUM_CASES)

customer_type = np.random.choice(
    ["SME", "Enterprise"],
    size=NUM_CASES,
    p=[0.7, 0.3]
)

region = np.random.choice(
    ["North", "South", "East", "West"],
    size=NUM_CASES
)

past_recovery_rate = np.round(
    np.random.uniform(0.3, 0.95, NUM_CASES), 2
)

dca_experience_score = np.round(
    np.random.uniform(0.4, 1.0, NUM_CASES), 2
)

previous_escalations = np.random.randint(0, 4, NUM_CASES)

# Business-driven recovery probability
base_prob = (
    0.4 * past_recovery_rate +
    0.3 * dca_experience_score -
    0.2 * (previous_escalations / 3) -
    0.1 * (days_overdue / 365)
)

base_prob = np.clip(base_prob, 0.05, 0.95)

recovered = np.random.binomial(1, base_prob)

df = pd.DataFrame({
    "case_id": case_id,
    "overdue_amount": overdue_amount,
    "days_overdue": days_overdue,
    "customer_type": customer_type,
    "region": region,
    "past_recovery_rate": past_recovery_rate,
    "dca_experience_score": dca_experience_score,
    "previous_escalations": previous_escalations,
    "recovered": recovered
})

df.to_csv("cases.csv", index=False)

print("Synthetic dataset generated: cases.csv")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("data/cases.csv")

# Encode categorical variables
le_customer = LabelEncoder()
le_region = LabelEncoder()

df["customer_type"] = le_customer.fit_transform(df["customer_type"])
df["region"] = le_region.fit_transform(df["region"])

# Features and target
X = df.drop(columns=["case_id", "recovered"])
y = df["recovered"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model (explainable, enterprise-friendly)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save artifacts
joblib.dump(model, "model/recovery_model.pkl")
joblib.dump(le_customer, "model/customer_encoder.pkl")
joblib.dump(le_region, "model/region_encoder.pkl")

print("Model and encoders saved successfully.")

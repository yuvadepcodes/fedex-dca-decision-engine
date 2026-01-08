import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_nexus_data(n=20):
    np.random.seed(42)

    business_types = ["Small", "Medium", "Enterprise"]
    dispute_statuses = ["None", "Open", "Resolved"]
    dcas = ["DCA Agent 1", "DCA Agent 2", "DCA Agent 3"]

    data = []
    for i in range(n):
        ageing = np.random.randint(1, 180)
        invoice_amount = np.random.randint(5000, 500000)
        business = random.choice(business_types)
        dispute = random.choice(dispute_statuses)
        assigned_dca = random.choice(dcas)

        last_update_days = np.random.randint(0, 15)
        last_update = datetime.now() - timedelta(days=last_update_days)

        sla_status = "BREACHED" if last_update_days > 2 else "OK"

        data.append({
            "case_id": f"CASE_{i+1}",
            "ageing_days": ageing,
            "invoice_amount": invoice_amount,
            "business_type": business,
            "dispute_status": dispute,
            "assigned_dca": assigned_dca,
            "last_dca_update_days": last_update_days,
            "sla_status": sla_status,
            "status": "ACTIVE"
        })

    df = pd.DataFrame(data)
    df.to_csv("data/nexus_accounts.csv", index=False)
    return df

if __name__ == "__main__":
    generate_nexus_data()

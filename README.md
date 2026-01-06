
An AI-driven decision and prioritization prototype for managing Debt Collection Agencies (DCAs) in large B2B enterprises like FedEx.

This project demonstrates the **core intelligence layer** of a scalable DCA management platform, focusing on:
- Case prioritization
- Recovery prediction
- Explainable decision-making
- Performance-aligned DCA allocation

---

## Problem Context

FedEx manages thousands of overdue B2B customer accounts through external Debt Collection Agencies (DCAs).  
Today, this process is largely manual, relying on spreadsheets, emails, and individual follow-ups, leading to:

- Limited visibility into recovery progress  
- Delayed escalations and weak accountability  
- No data-driven prioritization of cases  
- Minimal auditability and governance  

---

## Solution Overview

This prototype introduces an **AI-assisted decision engine** that acts as an orchestration layer between FedEx and its DCAs.

The system:
- Predicts recovery likelihood for each overdue case  
- Computes a business-driven priority score  
- Recommends optimal DCA allocation  
- Provides confidence and explainability for every decision  

> The focus is on **decision support**, not full automation.

---

## What This Prototype Demonstrates

- Synthetic but realistic case data generation  
- Explainable ML model for recovery prediction  
- Hybrid AI + rule-based prioritization logic  
- Human-in-the-loop friendly decision outputs  
- Foundation for scalable enterprise deployment  

---

## Repository Structure
fedex-dca-decision-engine/
│
├── data/ # Synthetic dataset and generation logic
├── model/ # ML training and prioritization logic
├── app/ # Streamlit demo application
├── docs/ # Architecture and process diagrams
├── requirements.txt
└── README.md

---

## Technology Stack

- Python  
- Pandas, NumPy  
- Scikit-learn  
- Streamlit  

The model prioritizes **explainability and governance** over raw accuracy, aligning with enterprise needs.

---

## Roadmap

**Phase 1 (Current Prototype)**  
- Core intelligence layer (prioritization & allocation)

**Phase 2**  
- Advanced ML models and feedback learning loops

**Phase 3**  
- Enterprise-grade workflow automation, dashboards, and integrations

---

## Disclaimer

All data used in this project is synthetic and created solely for demonstration purposes.

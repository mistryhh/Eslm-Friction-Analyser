# ESLM Friction Analyser 📊

**A "Service-First" Data Pipeline and Dashboard designed to optimise Enterprise Service Lifecycle Management (ESLM).**

---

## 🎯 Business Context

This project was built to demonstrate my ability to treat **"data as the bedrock"** of IT Service Management. Aligned with the operational goals of an enterprise IT environment, this tool automatically audits Configuration Items (CIs) for data quality issues and analyses service tickets to identify friction points when transitioning systems from **Pre-Live to Live** environments.

## 🚀 Key Insights Discovered

By running this pipeline on a simulated IT estate dataset, the tool successfully:
* **Improved Data Quality:** Identified 68 Configuration Items missing critical ownership data, automatically flagging them as `UNASSIGNED_REQUIRES_AUDIT` to reduce security/compliance risks.
* **Identified Systemic Friction Points:** Discovered that 'Pre-Live Transitions' take an average of **11.3 days**, significantly longer than Live Incidents (3.0 days).
* **Pinpointed Technological Bottlenecks:** Proved through relational data analysis that **Databases (13.5 days avg)** are the primary bottleneck slowing down the Pre-Live to Live deployment pipeline.

---

## 🛠️ Technical Architecture

* **Data Generation:** Python (`random`, `datetime`) to simulate messy, real-world enterprise data with intentional flaws.
* **Data Ingestion & Standardisation:** `pandas` to clean inputs and normalise taxonomy (e.g., standardising messy ticket statuses to 'Closed').
* **Data Analysis:** `pandas` to merge ticket data with the asset database and calculate Mean Time to Resolution (MTTR).
* **Insights Visualisation:** `streamlit` to present findings to technical and non-technical stakeholders in an accessible web dashboard.

---

## 📂 Repository Structure

```text
eslm-friction-analyser/
├── data/                      # (Git-ignored: Generated locally via script)
│   ├── raw/                   # Raw simulated datasets
│   └── processed/             # Cleaned datasets and insight reports
├── src/                       
│   ├── ingestion.py           # Pipeline Step 1: CI integrity and data quality control
│   └── analysis.py            # Pipeline Step 2: MTTR and bottleneck identification
├── app/                       
│   └── dashboard.py           # Pipeline Step 3: Streamlit visualization dashboard
├── generate_mock_data.py      # Run this first to build the "data bedrock"
├── requirements.txt           # Python dependencies
└── README.md
```


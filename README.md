# Congressional App Challenge – Attrition Analysis

## Context
The Congressional App Challenge (CAC) is a nationwide coding competition designed to encourage student engagement in computer science through district-level participation. While participation is widespread, not all registered teams ultimately submit a completed application. Understanding attrition—the failure to submit after registration—is important for improving program design, equity, and student outcomes.

This project analyzes participant-level CAC data to identify behavioral and socioeconomic factors associated with attrition. The goal is not prediction for its own sake, but to generate interpretable insights that can inform outreach, engagement strategies, and resource allocation.


## Methodology

### Data Sources

- CAC participation data (2015–present prototype subset):
  - Registration timestamps
  - Submission timestamps
  - Team size
  - ZIP code

- U.S. Census American Community Survey (ACS) 5-Year Data:
  - Median household income (ZIP Code Tabulation Area level)
  - Proxy indicators for low-income and rural areas

### Data Pipeline

An end-to-end, reproducible pipeline was constructed:

1. Raw CSV ingestion with schema validation
2. Data cleaning and type normalization
3. ZIP code correction and geographic standardization
4. Binary label construction (attrition)
5. External Census data enrichment via API
6. Feature engineering for behavioral timing variables

### Modeling Approach

- **Binary classification using logistic regression**
- Chosen for interpretability and policy relevance
- Two models estimated:
  - Baseline model (behavioral factors only)
  - Census-augmented model (adds socioeconomic controls)
**
Model outputs are reported as odds ratios, enabling direct interpretation of effect direction and magnitude.**

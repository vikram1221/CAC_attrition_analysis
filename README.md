# Congressional App Challenge – Attrition Analysis

## Context
The Congressional App Challenge (CAC) is a nationwide coding competition designed to encourage student engagement in computer science through district-level participation. While participation is widespread, not all registered teams ultimately submit a completed application. Understanding attrition - the failure to submit after registration - is important for improving program design, equity, and student outcomes.

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

**Model outputs are reported as odds ratios, enabling direct interpretation of effect direction and magnitude.**


## Key Outcomes


<img width="998" height="616" alt="visualisations" src="https://github.com/user-attachments/assets/d92cdab0-3b85-4d85-a8b8-fee66f163b75" />

### Behavioral Effects (Robust Across Models)

Across both the baseline and Census-augmented logistic regression models, behavioral engagement variables emerge as the strongest predictors of attrition.

- **Team size**:
In the baseline model, each additional team member is associated with a 39% reduction in attrition odds (odds ratio ≈ 0.61). After adjusting for Census socioeconomic variables, the effect remains strong, with a 33% reduction in attrition odds (odds ratio ≈ 0.67).

- **Registration timing (month)**:
Later registration substantially increases attrition risk. The baseline model estimates nearly a 95% increase in attrition odds per unit increase in registration month (odds ratio ≈ 1.95). After Census adjustment, the effect remains pronounced, with attrition odds increasing by approximately 68% (odds ratio ≈ 1.68).

- **Registration day of week**:
Day-of-week effects are small and unstable across models (odds ratios ≈ 1.20–1.22) and are not interpreted as primary drivers of attrition.

These results indicate that early engagement and collaborative participation play a central role in reducing attrition, independent of geographic or socioeconomic context.


### Socioeconomic Context

The Census-augmented model incorporates ZIP code–level socioeconomic controls to assess whether behavioral effects are confounded by geography or income.

- Median household income enters with an odds ratio of approximately 0.61, indicating that participants from higher-income areas have substantially lower attrition risk, holding behavioral factors constant.

- Rural proxy effects are modest and inconclusive (odds ratio ≈ 0.83) and are sensitive to missing geographic information in the prototype sample.

- A low-income area indicator exhibits no detectable association with attrition (odds ratio ≈ 1.00) in this small-scale analysis.


## Recommendations for the Congressional App Challenge

1. **Encourage early registration**
Later registration is consistently associated with higher attrition. CAC could implement early-registration incentives, reminder campaigns, or milestone check-ins for participants who register closer to deadlines.

2. **Promote team-based participation**
Larger team sizes are strongly associated with lower attrition across all models. Facilitating team formation—through school outreach, mentor matching, or collaboration tools—may improve completion rates.

3. **Target outreach beyond behavioral signals**
While socioeconomic context matters, behavioral engagement factors remain predictive even after Census adjustment. This suggests that engagement-focused interventions can be effective across districts, including lower-income areas.

4. **Provide additional support for participants with limited geographic information**
Participants with missing or incomplete geographic data exhibit different attrition patterns. CAC may benefit from targeted follow-ups or onboarding support for these participants to ensure access barriers are addressed early.

5. **Scale analysis with full participation data**
Applying this pipeline to the complete CAC dataset would enable statistically robust estimates and allow CAC to identify district-level or cohort-specific patterns, supporting more targeted program design.

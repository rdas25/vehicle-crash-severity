# Crash Injury Severity Predictor

Predicts the severity of injuries in vehicle crashes using historical NHTSA/FARS
(Fatality Analysis Reporting System) data, with an eye toward how this kind of
risk scoring could inform insurance premium pricing.

## What it does

- Merges and cleans multiple NHTSA/FARS datasets into a single modeling-ready table
- Engineers features from raw crash records (vehicle, driver, and environmental factors)
- Trains a Random Forest classifier to predict injury severity
- Outputs a risk score per record that could feed into a premium-pricing model

## Why I built it

I got interested in the intersection of transportation safety and data science
through [pedestrian/transportation safety work — link your Youth Voices for a Sober
Future or pedestrian safety app project here if you want to cross-reference it].
This project was a chance to work with real federal crash data and see what
actually predicts severity outcomes, rather than just building a toy dataset model.

## Tech stack

- Python, pandas, scikit-learn (RandomForestClassifier)
- Jupyter/VS Code interactive cells for exploration and iteration

## Challenges & what I learned

- Merging FARS's multiple linked tables (crash, vehicle, person-level records) without
  losing or duplicating rows
- Handling inconsistent dtypes across years of NHTSA data
- Working around GitHub's file size limits for the raw dataset (solution: [describe
  briefly — e.g. "stored a sampled/processed subset and documented the full download
  source instead"])

## Data source

[Link to NHTSA/FARS dataset]

## Running it

\`\`\`bash
pip install -r requirements.txt
jupyter notebook crash_severity_model.ipynb
\`\`\`

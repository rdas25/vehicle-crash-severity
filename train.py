# %% --- Cell 1: Imports ---
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix, f1_score
)
from sklearn.metrics import roc_auc_score
import joblib

# %% --- Cell 2: Load and merge (same as explore.py) ---
accident = pd.read_csv("/Users/rohandasanoor/Downloads/FARS2024NationalCSV/accident.csv")
person   = pd.read_csv("/Users/rohandasanoor/Downloads/FARS2024NationalCSV/person.csv")

df = person.merge(
    accident[[
        'ST_CASE', 'YEAR', 'DAY_WEEK', 'WEATHER', 'WEATHERNAME',
        'LGT_COND', 'LGT_CONDNAME', 'RD_OWNER', 'RD_OWNERNAME',
        'NHS', 'NHSNAME', 'RELJCT2', 'RELJCT2NAME', 'REL_ROAD',
        'REL_ROADNAME', 'WRK_ZONE', 'WRK_ZONENAME', 'LATITUDE',
        'LONGITUD', 'FATALS', 'PERSONS', 'VE_TOTAL', 'PEDS',
        'TYP_INT', 'TYP_INTNAME', 'SP_JUR', 'SP_JURNAME'
    ]],
    on='ST_CASE',
    how='left'
)

# Filter to valid severity codes only
df = df[df['INJ_SEV'].isin([0, 1, 2, 3, 4])].copy()
print(f"Rows after merge and filter: {len(df):,}")

# %% --- Cell 3: Drop leakage and irrelevant columns ---
drop_cols = [
    # Post-crash info (leakage)
    'DEATH_MO', 'DEATH_MONAME', 'DEATH_DA', 'DEATH_DANAME',
    'DEATH_YR', 'DEATH_YRNAME', 'DEATH_TM', 'DEATH_TMNAME',
    'DEATH_HR', 'DEATH_HRNAME', 'DEATH_MN', 'DEATH_MNNAME',
    'LAG_HRS',  'LAG_HRSNAME',  'LAG_MINS', 'LAG_MINSNAME',
    'HOSPITAL', 'HOSPITALNAME', 'DOA',       'DOANAME',
    'FATALS',

    # Redundant label columns (keep numeric codes for modeling)
    'INJ_SEVNAME', 'AGENAME', 'STATENAME', 'SEXNAME',
    'HOURNAME', 'MINUTENAME', 'MONTHNAME', 'DAYNAME',
    'WEATHERNAME', 'LGT_CONDNAME', 'RUR_URBNAME', 'FUNC_SYSNAME',
    'HARM_EVNAME', 'MAN_COLLNAME', 'SCH_BUSNAME', 'RD_OWNERNAME',
    'NHSNAME', 'RELJCT2NAME', 'REL_ROADNAME', 'WRK_ZONENAME',
    'TYP_INTNAME', 'SP_JURNAME', 'ROLLOVERNAME', 'IMPACT1NAME',
    'FIRE_EXPNAME', 'TOW_VEHNAME', 'SPEC_USENAME', 'EMER_USENAME',
    'BODY_TYPNAME', 'ICFINALBODYNAME', 'GVWR_FROMNAME', 'GVWR_TONAME',
    'MOD_YEARNAME', 'VPICMAKENAME', 'VPICMODELNAME', 'VPICBODYCLASSNAME',
    'MAKENAME', 'MAK_MODNAME', 'SEAT_POSNAME', 'REST_USENAME',
    'REST_MISNAME', 'HELM_USENAME', 'HELM_MISNAME', 'AIR_BAGNAME',
    'EJECTIONNAME', 'EJ_PATHNAME', 'EXTRICATNAME', 'DRINKINGNAME',
    'ALC_STATUSNAME', 'ATST_TYPNAME', 'ALC_RESNAME', 'DRUGSNAME',
    'DSTATUSNAME', 'DEVTYPENAME', 'DEVMOTORNAME', 'LOCATIONNAME',
    'WORK_INJNAME', 'HISPANICNAME', 'PER_TYPNAME', 'DAY_WEEKNAME',
    'COUNTYNAME', 'CITYNAME', 'ROUTENAME', 'LATITUDENAME',
    'LONGITUDNAME', 'MILEPTNAME',

    # IDs and free text (not useful as features)
    'ST_CASE', 'VEH_NO', 'PER_NO',
]

# Only drop columns that actually exist in df
drop_cols = [c for c in drop_cols if c in df.columns]
df = df.drop(columns=drop_cols)

print(f"Columns remaining: {df.shape[1]}")
print(df.columns.tolist())

# %% --- Cell 4: Handle nulls ---
# The 9,004 vehicle nulls are non-occupants (pedestrians etc.)
# Fill numeric nulls with -1 so the model treats them as a distinct category
df = df.fillna(-1)

print("Nulls remaining:", df.isnull().sum().sum())

# %% --- Cell 5: Define features and target ---
TARGET = 'INJ_SEV'

X = df.drop(columns=[TARGET])
y = df[TARGET]

print(f"Features: {X.shape[1]}")
print(f"Samples:  {len(y):,}")
print(f"\nClass distribution:")
for val, count in y.value_counts().sort_index().items():
    print(f"  {val}: {count:>7,} ({count/len(y)*100:.1f}%)")

# %% --- Cell 6: Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
    # stratify=y ensures each split has the same class proportions
)

print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# %% --- Cell 7: Train Random Forest with class weights ---
# class_weight='balanced' tells the model to penalize
# misclassifying rare classes (minor, possible) more heavily
print("Training Random Forest...")
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=4,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1          # use all CPU cores
)
rf.fit(X_train, y_train)
print("Done.")

# %% --- Cell 8: Evaluate ---
y_pred = rf.predict(X_test)

print("Classification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=['No Injury','Possible','Minor','Serious','Fatal']
))

proba = rf.predict_proba(X_test)

# One-vs-rest, macro-averaged (each class weighted equally)
auc_macro = roc_auc_score(y_test, proba, multi_class='ovr', average='macro')

# One-vs-rest, weighted by class support
auc_weighted = roc_auc_score(y_test, proba, multi_class='ovr', average='weighted')

print(f"Macro OvR AUC:    {auc_macro:.4f}")
print(f"Weighted OvR AUC: {auc_weighted:.4f}")

# %% --- Cell 9: Confusion matrix ---
cm = pd.DataFrame(
    confusion_matrix(y_test, y_pred),
    index  =['True: No Inj','True: Possible','True: Minor','True: Serious','True: Fatal'],
    columns=['Pred: No Inj','Pred: Possible','Pred: Minor','Pred: Serious','Pred: Fatal']
)
print("Confusion Matrix:")
print(cm)

# %% --- Cell 10: Feature importances ---
importances = pd.Series(rf.feature_importances_, index=X.columns)
print("Top 20 most important features:")
print(importances.sort_values(ascending=False).head(20))

# %% --- Cell 11: Insurance risk scoring ---
# predict_proba gives probability for each class [0,1,2,3,4]
# weighted sum gives a continuous severity score 0.0-4.0
proba = rf.predict_proba(X_test)
weights = np.array([0, 1, 2, 3, 4])
severity_score = (proba * weights).sum(axis=1)

# Scale to 0-100 for insurance pricing
risk_score = (severity_score / 4.0) * 100

def get_premium(base_premium, risk_score):
    if   risk_score < 25: multiplier = 0.85
    elif risk_score < 50: multiplier = 1.00
    elif risk_score < 70: multiplier = 1.35
    elif risk_score < 85: multiplier = 1.75
    else:                 multiplier = 2.50
    return {
        'risk_score':       round(risk_score, 1),
        'multiplier':       multiplier,
        'annual_premium':   round(base_premium * multiplier, 2),
        'monthly_premium':  round(base_premium * multiplier / 12, 2)
    }

# Show sample pricing for first 10 test cases
print("Sample insurance pricing (base premium = $1,200/yr):")
print(f"{'Risk Score':>12} {'Band':>10} {'Annual':>10} {'Monthly':>10}")
print("-" * 46)
for score in risk_score[:10]:
    p = get_premium(1200, score)
    print(f"{p['risk_score']:>12} {p['multiplier']:>10} ${p['annual_premium']:>9} ${p['monthly_premium']:>9}")

# %% --- Cell 12: Save the model ---
joblib.dump(rf, "/Users/rohandasanoor/Documents/GitHub/vehicle-crash-severity/models")
print("Model saved to /Users/rohandasanoor/Documents/GitHub/vehicle-crash-severity/models")
